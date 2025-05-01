import os
import logging
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from utils.pronunciation import generate_pronunciation
from utils.examples import generate_examples_for_word

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Configure the database
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///app.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

# Create database tables
with app.app_context():
    # Import models to register them with SQLAlchemy
    import models
    # Create tables
    db.create_all()
    app.logger.info("Database tables created")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Lütfen devam etmek için giriş yapın.'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Main routes
@app.route("/")
def index():
    """Render the main quiz application page"""
    return render_template("index.html")

@app.route("/qr")
def qr_code():
    """Render QR code page for mobile access"""
    return render_template("qr.html")

@app.route("/leaderboard")
def leaderboard():
    """Show leaderboard page"""
    return render_template("leaderboard.html")

@app.route("/favorites")
@login_required
def user_favorites():
    """Show user favorites page"""
    return render_template("favorites.html")

@app.route("/review")
@login_required
def review():
    """Show spaced repetition review page"""
    return render_template("review.html")

# Auth routes
@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login"""
    if request.method == "POST":
        from models import User
        
        username = request.form.get("username")
        password = request.form.get("password")
        remember = 'remember' in request.form
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            next_page = request.args.get('next')
            if not next_page or next_page.startswith('/'):
                next_page = url_for('index')
                
            return redirect(next_page)
        else:
            flash("Geçersiz kullanıcı adı veya şifre.")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration"""
    if request.method == "POST":
        from models import User
        
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Validate form data
        if not username or not email or not password:
            flash("Tüm alanları doldurmalısınız.")
            return render_template("register.html")
        
        if password != confirm_password:
            flash("Şifreler uyuşmuyor.")
            return render_template("register.html")
        
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Bu kullanıcı adı veya e-posta zaten kullanılıyor.")
            return render_template("register.html")
        
        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    return redirect(url_for("index"))

# API routes for the quiz application
@app.route("/api/words")
def get_words():
    """Return Oxford word lists"""
    word_list = request.args.get("list", "oxford3000")
    
    # Load words from database if available
    from models import Word
    words = Word.query.filter_by(word_list=word_list).all()
    
    if words:
        return jsonify([{
            "id": word.id,
            "english": word.english, 
            "turkish": word.turkish,
            "word_list": word.word_list
        } for word in words])
    
    # If database is empty, load from JSON files
    try:
        with open(f"static/data/{word_list}.json", "r", encoding="utf-8") as f:
            words = json.load(f)
            return jsonify(words)
    except Exception as e:
        app.logger.error(f"Error loading word list: {e}")
        return jsonify({"error": "Failed to load word list"}), 500

@app.route("/api/favorites", methods=["GET", "POST", "DELETE"])
@login_required
def favorites():
    """Handle user favorites"""
    from models import Favorite, Word
    
    if request.method == "GET":
        user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        favorite_words = []
        
        for fav in user_favorites:
            word = Word.query.get(fav.word_id)
            if word:
                favorite_words.append({
                    "id": word.id,
                    "english": word.english,
                    "turkish": word.turkish,
                    "word_list": word.word_list,
                    "favorite_id": fav.id
                })
        
        return jsonify(favorite_words)
    
    elif request.method == "POST":
        data = request.get_json()
        english = data.get("english")
        turkish = data.get("turkish")
        
        # Find or create the word
        word = Word.query.filter_by(english=english, turkish=turkish).first()
        if not word:
            word_list = data.get("word_list", "oxford3000")
            word = Word(english=english, turkish=turkish, word_list=word_list)
            db.session.add(word)
            db.session.flush()
        
        # Check if already favorited
        existing_favorite = Favorite.query.filter_by(user_id=current_user.id, word_id=word.id).first()
        if existing_favorite:
            return jsonify({"message": "Already in favorites"}), 200
        
        # Add to favorites
        favorite = Favorite(user_id=current_user.id, word_id=word.id)
        db.session.add(favorite)
        db.session.commit()
        
        return jsonify({
            "message": "Added to favorites",
            "favorite_id": favorite.id,
            "word_id": word.id
        }), 201
    
    elif request.method == "DELETE":
        data = request.get_json()
        favorite_id = data.get("favorite_id")
        
        if not favorite_id:
            return jsonify({"error": "No favorite_id provided"}), 400
        
        favorite = Favorite.query.filter_by(id=favorite_id, user_id=current_user.id).first()
        if not favorite:
            return jsonify({"error": "Favorite not found"}), 404
        
        db.session.delete(favorite)
        db.session.commit()
        
        return jsonify({"message": "Removed from favorites"}), 200

@app.route("/api/quiz-results", methods=["POST"])
@login_required
def save_quiz_results():
    """Save quiz results to the database"""
    from models import QuizAttempt, QuizAnswer, Word, UserStat
    
    data = request.get_json()
    
    # Create quiz attempt
    quiz_attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_mode=data.get("mode", "en-tr"),
        difficulty=data.get("difficulty", "easy"),
        word_list=data.get("wordList", "oxford3000"),
        question_count=len(data.get("questions", [])),
        correct_count=data.get("score", 0),
        time_taken=data.get("timeTaken")
    )
    
    db.session.add(quiz_attempt)
    db.session.flush()  # Get ID without committing
    
    # Add individual answers
    for q in data.get("questions", []):
        # Find or create the word
        english = q.get("word")
        turkish = q.get("translation")
        
        word = Word.query.filter_by(english=english, turkish=turkish).first()
        if not word:
            word = Word(
                english=english, 
                turkish=turkish, 
                word_list=data.get("wordList", "oxford3000")
            )
            db.session.add(word)
            db.session.flush()
        
        # Create answer record
        answer = QuizAnswer(
            quiz_attempt_id=quiz_attempt.id,
            word_id=word.id,
            is_correct=q.get("correct", False),
            time_taken=q.get("timeTaken")
        )
        db.session.add(answer)
        
        # Update user stats for spaced repetition
        user_stat = UserStat.query.filter_by(user_id=current_user.id, word_id=word.id).first()
        if not user_stat:
            user_stat = UserStat(user_id=current_user.id, word_id=word.id)
            db.session.add(user_stat)
        
        # Update stats
        user_stat.last_reviewed = datetime.utcnow()
        
        if q.get("correct", False):
            user_stat.correct_count += 1
            # Increase ease factor if correct (spaced repetition algorithm)
            user_stat.ease_factor = min(user_stat.ease_factor + 0.1, 2.5)
            
            # Calculate next interval based on SM-2 algorithm
            if user_stat.interval == 0:
                user_stat.interval = 1
            elif user_stat.interval == 1:
                user_stat.interval = 6
            else:
                user_stat.interval = int(user_stat.interval * user_stat.ease_factor)
        else:
            user_stat.incorrect_count += 1
            # Decrease ease factor if wrong
            user_stat.ease_factor = max(user_stat.ease_factor - 0.2, 1.3)
            # Reset interval
            user_stat.interval = 1
        
        # Calculate next review date
        user_stat.next_review = datetime.utcnow() + timedelta(days=user_stat.interval)
    
    # Commit all changes
    db.session.commit()
    
    return jsonify({"message": "Quiz results saved", "quiz_id": quiz_attempt.id}), 201

@app.route("/api/stats")
@login_required
def get_user_stats():
    """Get user statistics"""
    from models import QuizAttempt, UserStat, Word
    
    # Get overall stats
    quiz_count = QuizAttempt.query.filter_by(user_id=current_user.id).count()
    
    if quiz_count == 0:
        return jsonify({
            "completed_quizzes": 0,
            "learned_words": 0,
            "success_rate": 0,
            "average_time": 0,
            "due_for_review": 0
        })
    
    total_score = db.session.query(db.func.sum(QuizAttempt.correct_count)).filter_by(user_id=current_user.id).scalar() or 0
    total_questions = db.session.query(db.func.sum(QuizAttempt.question_count)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Calculate learned words (words with more correct than incorrect answers)
    learned_stats = UserStat.query.filter(
        UserStat.user_id == current_user.id,
        UserStat.correct_count > UserStat.incorrect_count
    ).count()
    
    # Calculate due for review
    due_for_review = UserStat.query.filter(
        UserStat.user_id == current_user.id,
        UserStat.next_review <= datetime.utcnow()
    ).count()
    
    # Calculate average time per question
    avg_time_results = db.session.query(
        db.func.avg(QuizAttempt.time_taken / QuizAttempt.question_count)
    ).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.time_taken.isnot(None)
    ).first()
    
    avg_time = round(avg_time_results[0] or 0, 1)
    
    # Success rate
    success_rate = int((total_score / total_questions * 100) if total_questions > 0 else 0)
    
    return jsonify({
        "completed_quizzes": quiz_count,
        "learned_words": learned_stats,
        "success_rate": success_rate,
        "average_time": avg_time,
        "due_for_review": due_for_review
    })

@app.route("/api/leaderboard")
def get_leaderboard():
    """Get leaderboard data"""
    from models import User, QuizAttempt
    from sqlalchemy import func
    
    # Get top 10 users by success rate (minimum 5 quizzes)
    leaderboard = db.session.query(
        User.username,
        func.count(QuizAttempt.id).label('quiz_count'),
        func.sum(QuizAttempt.correct_count).label('correct_count'),
        func.sum(QuizAttempt.question_count).label('question_count'),
        (func.sum(QuizAttempt.correct_count) * 100 / func.sum(QuizAttempt.question_count)).label('success_rate'),
        func.avg(QuizAttempt.time_taken / QuizAttempt.question_count).label('avg_time')
    ).join(QuizAttempt).group_by(User.id).having(
        func.count(QuizAttempt.id) >= 5
    )
    
    # Apply time period filter
    period = request.args.get('period', 'all')
    if period == 'week':
        week_ago = datetime.utcnow() - timedelta(days=7)
        leaderboard = leaderboard.filter(QuizAttempt.created_at >= week_ago)
    elif period == 'month':
        month_ago = datetime.utcnow() - timedelta(days=30)
        leaderboard = leaderboard.filter(QuizAttempt.created_at >= month_ago)
    
    # Apply leaderboard type filter and order
    board_type = request.args.get('type', 'success_rate')
    if board_type == 'success_rate':
        leaderboard = leaderboard.order_by(((func.sum(QuizAttempt.correct_count) * 100) / func.cast(func.sum(QuizAttempt.question_count), db.Numeric)).desc())
    elif board_type == 'words_learned':
        leaderboard = leaderboard.order_by(func.sum(QuizAttempt.correct_count).desc())
    elif board_type == 'quiz_count':
        leaderboard = leaderboard.order_by(func.count(QuizAttempt.id).desc())
    elif board_type == 'speed':
        leaderboard = leaderboard.filter(QuizAttempt.time_taken.isnot(None)).order_by(func.avg(QuizAttempt.time_taken / func.cast(QuizAttempt.question_count, db.Numeric)).asc())
    
    # Execute query and limit to top 10
    results = leaderboard.limit(10).all()
    
    # Format results
    formatted_results = []
    for result in results:
        formatted_results.append({
            'username': result.username,
            'quiz_count': result.quiz_count,
            'success_rate': round(result.success_rate),
            'word_count': result.correct_count,
            'words_learned': result.correct_count,
            'avg_time': round(result.avg_time, 1) if result.avg_time else None
        })
    
    return jsonify(formatted_results)

@app.route("/api/words-for-review")
@login_required
def get_words_for_review():
    """Get words that are due for review"""
    from models import UserStat, Word
    
    # Find words due for review
    stats = UserStat.query.filter(
        UserStat.user_id == current_user.id,
        UserStat.next_review <= datetime.utcnow()
    ).order_by(UserStat.next_review).limit(100).all()
    
    words_for_review = []
    for stat in stats:
        word = Word.query.get(stat.word_id)
        if word:
            words_for_review.append({
                'id': word.id,
                'english': word.english,
                'turkish': word.turkish,
                'word_list': word.word_list,
                'stat_id': stat.id,
                'ease_factor': stat.ease_factor,
                'interval': stat.interval
            })
    
    return jsonify(words_for_review)

@app.route("/api/review-feedback", methods=["POST"])
@login_required
def submit_review_feedback():
    """Handle feedback from review sessions"""
    from models import UserStat, Word
    
    data = request.get_json()
    word_id = data.get('word_id')
    feedback = data.get('feedback', 'medium')
    
    # Find the user stat
    user_stat = UserStat.query.filter_by(user_id=current_user.id, word_id=word_id).first()
    
    if not user_stat:
        return jsonify({'error': 'Word not found in user stats'}), 404
    
    # Update based on feedback
    user_stat.last_reviewed = datetime.utcnow()
    
    # Adjust ease factor and interval based on feedback
    if feedback == 'easy':
        user_stat.correct_count += 1
        user_stat.ease_factor = min(user_stat.ease_factor + 0.15, 2.5)
        if user_stat.interval == 0:
            user_stat.interval = 2
        else:
            user_stat.interval = int(user_stat.interval * user_stat.ease_factor)
            
    elif feedback == 'good':
        user_stat.correct_count += 1
        user_stat.ease_factor = min(user_stat.ease_factor + 0.1, 2.5)
        if user_stat.interval == 0:
            user_stat.interval = 1
        else:
            user_stat.interval = int(user_stat.interval * user_stat.ease_factor)
            
    elif feedback == 'medium':
        # Neutral response - small increase but shorter interval
        user_stat.correct_count += 1
        if user_stat.interval == 0:
            user_stat.interval = 1
        else:
            user_stat.interval = max(1, int(user_stat.interval * 0.8))
            
    elif feedback == 'hard':
        user_stat.incorrect_count += 1
        user_stat.ease_factor = max(user_stat.ease_factor - 0.2, 1.3)
        user_stat.interval = 1  # Reset interval for hard words
    
    # Calculate next review date
    user_stat.next_review = datetime.utcnow() + timedelta(days=user_stat.interval)
    
    # Save changes
    db.session.commit()
    
    return jsonify({
        'success': True,
        'next_review': user_stat.next_review.isoformat(),
        'new_interval': user_stat.interval
    })

@app.route("/api/pronunciation")
def get_pronunciation():
    """Generate and return pronunciation for a word"""
    word = request.args.get('word')
    
    if not word:
        return jsonify({'error': 'No word provided'}), 400
    
    from models import Word
    
    # Check if we have a stored pronunciation URL
    word_record = Word.query.filter_by(english=word).first()
    
    if word_record and word_record.pronunciation_url:
        return redirect(word_record.pronunciation_url)
    
    # Generate new pronunciation
    pronunciation_url = generate_pronunciation(word)
    
    if not pronunciation_url:
        return jsonify({'error': 'Failed to generate pronunciation'}), 500
    
    # Store URL if we have a word record
    if word_record:
        word_record.pronunciation_url = pronunciation_url
        db.session.commit()
    
    # Serve the audio file
    try:
        return send_file(pronunciation_url, mimetype='audio/mpeg')
    except Exception as e:
        app.logger.error(f"Error serving pronunciation file: {e}")
        return jsonify({'error': 'Failed to serve pronunciation file'}), 500

@app.route("/api/examples")
def get_examples():
    """Get example sentences for a word"""
    word = request.args.get('word')
    
    if not word:
        return jsonify({'error': 'No word provided'}), 400
    
    from models import Word, ExampleSentence
    
    # Check if we have stored examples
    word_record = Word.query.filter_by(english=word).first()
    
    if word_record:
        stored_examples = ExampleSentence.query.filter_by(word_id=word_record.id).all()
        
        if stored_examples:
            return jsonify([{
                'english_sentence': example.english_sentence,
                'turkish_sentence': example.turkish_sentence
            } for example in stored_examples])
    
    # Generate new examples
    examples = generate_examples_for_word(word)
    
    # Store examples if we have a word record
    if word_record and examples:
        for example in examples:
            example_record = ExampleSentence(
                word_id=word_record.id,
                english_sentence=example['english_sentence'],
                turkish_sentence=example['turkish_sentence']
            )
            db.session.add(example_record)
        db.session.commit()
    
    return jsonify(examples)

# Initialize database and create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

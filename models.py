from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy='dynamic')
    favorites = db.relationship('Favorite', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    english = db.Column(db.String(100), nullable=False)
    turkish = db.Column(db.String(100), nullable=False)
    word_list = db.Column(db.String(20), nullable=False)  # 'oxford3000' or 'oxford5000'
    pronunciation_url = db.Column(db.String(255))  # URL to the pronunciation audio file
    
    # Relationships
    favorites = db.relationship('Favorite', backref='word', lazy='dynamic')
    quiz_answers = db.relationship('QuizAnswer', backref='word', lazy='dynamic')
    examples = db.relationship('ExampleSentence', backref='word', lazy='dynamic')
    
    def __repr__(self):
        return f'<Word {self.english} - {self.turkish}>'
        
class ExampleSentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    english_sentence = db.Column(db.Text, nullable=False)
    turkish_sentence = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<ExampleSentence {self.id} for word_id {self.word_id}>'

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Favorite {self.user_id} - {self.word_id}>'

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_mode = db.Column(db.String(10), nullable=False)  # 'en-tr' or 'tr-en'
    difficulty = db.Column(db.String(10), nullable=False)  # 'easy', 'medium', 'hard'
    word_list = db.Column(db.String(20), nullable=False)  # 'oxford3000', 'oxford5000', or 'combined'
    question_count = db.Column(db.Integer, nullable=False)
    correct_count = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer)  # in seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    answers = db.relationship('QuizAnswer', backref='quiz_attempt', lazy='dynamic')
    
    def __repr__(self):
        return f'<QuizAttempt {self.id} - {self.user_id}>'

class QuizAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempt.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    time_taken = db.Column(db.Float)  # in seconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<QuizAnswer {self.id} - {self.quiz_attempt_id}>'

class UserStat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    correct_count = db.Column(db.Integer, default=0)
    incorrect_count = db.Column(db.Integer, default=0)
    
    # Spaced repetition fields
    last_reviewed = db.Column(db.DateTime)
    next_review = db.Column(db.DateTime)
    ease_factor = db.Column(db.Float, default=2.5)  # Used in spaced repetition algorithm
    interval = db.Column(db.Integer, default=0)  # Days between reviews
    
    def __repr__(self):
        return f'<UserStat {self.user_id} - {self.word_id}>'
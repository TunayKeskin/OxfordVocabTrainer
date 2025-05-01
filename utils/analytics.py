from datetime import datetime, timedelta
from sqlalchemy import func, extract, cast, String, and_, or_, desc, asc
from models import QuizAttempt, QuizAnswer, Word, UserStat


def get_user_progress_over_time(user_id, days=30):
    """
    Get the user's progress over time, showing accuracy and quiz counts by day
    
    Args:
        user_id (int): The ID of the user
        days (int): Number of days to look back
        
    Returns:
        dict: Dictionary with dates and corresponding stats
    """
    from app import db
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get daily quiz stats
    daily_stats = db.session.query(
        func.date(QuizAttempt.created_at).label('date'),
        func.count().label('quiz_count'),
        func.sum(QuizAttempt.correct_count).label('correct_count'),
        func.sum(QuizAttempt.question_count).label('total_questions'),
        func.avg(QuizAttempt.correct_count * 100 / QuizAttempt.question_count).label('accuracy')
    ).filter(
        QuizAttempt.user_id == user_id,
        QuizAttempt.created_at >= start_date
    ).group_by(
        func.date(QuizAttempt.created_at)
    ).order_by(
        func.date(QuizAttempt.created_at)
    ).all()
    
    # Convert to a dictionary with ISO format dates
    result = {
        "dates": [],
        "quiz_counts": [],
        "accuracies": []
    }
    
    for stat in daily_stats:
        result["dates"].append(stat.date.isoformat())
        result["quiz_counts"].append(stat.quiz_count)
        result["accuracies"].append(round(stat.accuracy or 0, 2))
        
    return result


def get_quiz_type_breakdown(user_id):
    """
    Get the breakdown of quiz types taken by the user
    
    Args:
        user_id (int): The ID of the user
        
    Returns:
        dict: Dictionary with quiz types and counts
    """
    from app import db
    
    # Get stats by quiz mode
    mode_stats = db.session.query(
        QuizAttempt.quiz_mode,
        func.count().label('count')
    ).filter(
        QuizAttempt.user_id == user_id
    ).group_by(
        QuizAttempt.quiz_mode
    ).all()
    
    # Get stats by difficulty
    difficulty_stats = db.session.query(
        QuizAttempt.difficulty,
        func.count().label('count')
    ).filter(
        QuizAttempt.user_id == user_id
    ).group_by(
        QuizAttempt.difficulty
    ).all()
    
    # Get stats by word list
    wordlist_stats = db.session.query(
        QuizAttempt.word_list,
        func.count().label('count')
    ).filter(
        QuizAttempt.user_id == user_id
    ).group_by(
        QuizAttempt.word_list
    ).all()
    
    return {
        "modes": {stat.quiz_mode: stat.count for stat in mode_stats},
        "difficulties": {stat.difficulty: stat.count for stat in difficulty_stats},
        "word_lists": {stat.word_list: stat.count for stat in wordlist_stats}
    }


def get_user_word_mastery(user_id):
    """
    Get the user's word mastery breakdown
    
    Args:
        user_id (int): The ID of the user
        
    Returns:
        dict: Dictionary with word mastery stats
    """
    from app import db
    
    # Calculate word mastery levels
    word_stats = db.session.query(
        UserStat.word_id,
        Word.english,
        Word.turkish,
        UserStat.correct_count,
        UserStat.incorrect_count,
        UserStat.ease_factor,
        (cast(UserStat.correct_count, String) + ' / ' + 
         cast(UserStat.correct_count + UserStat.incorrect_count, String)).label('ratio'),
        (UserStat.correct_count * 100 / 
         (UserStat.correct_count + UserStat.incorrect_count)).label('percentage')
    ).join(Word, Word.id == UserStat.word_id).filter(
        UserStat.user_id == user_id,
        or_(UserStat.correct_count > 0, UserStat.incorrect_count > 0)
    ).order_by(
        desc('percentage'),
        desc(UserStat.correct_count)
    ).limit(50).all()
    
    mastered = []
    learning = []
    challenging = []
    
    for stat in word_stats:
        word_data = {
            "word_id": stat.word_id,
            "english": stat.english,
            "turkish": stat.turkish,
            "correct": stat.correct_count,
            "incorrect": stat.incorrect_count,
            "ratio": stat.ratio,
            "percentage": round(stat.percentage or 0, 1),
            "ease_factor": round(stat.ease_factor, 2) if stat.ease_factor else 2.5
        }
        
        if stat.percentage >= 90:
            mastered.append(word_data)
        elif stat.percentage >= 60:
            learning.append(word_data)
        else:
            challenging.append(word_data)
    
    # Get counts
    mastered_count = db.session.query(func.count()).select_from(UserStat).filter(
        UserStat.user_id == user_id,
        (UserStat.correct_count * 100 / (UserStat.correct_count + UserStat.incorrect_count)) >= 90,
        UserStat.correct_count + UserStat.incorrect_count > 0
    ).scalar() or 0
    
    learning_count = db.session.query(func.count()).select_from(UserStat).filter(
        UserStat.user_id == user_id,
        (UserStat.correct_count * 100 / (UserStat.correct_count + UserStat.incorrect_count)) >= 60,
        (UserStat.correct_count * 100 / (UserStat.correct_count + UserStat.incorrect_count)) < 90,
        UserStat.correct_count + UserStat.incorrect_count > 0
    ).scalar() or 0
    
    challenging_count = db.session.query(func.count()).select_from(UserStat).filter(
        UserStat.user_id == user_id,
        (UserStat.correct_count * 100 / (UserStat.correct_count + UserStat.incorrect_count)) < 60,
        UserStat.correct_count + UserStat.incorrect_count > 0
    ).scalar() or 0
    
    return {
        "mastery_counts": {
            "mastered": mastered_count,
            "learning": learning_count,
            "challenging": challenging_count
        },
        "top_words": {
            "mastered": mastered[:10],
            "learning": learning[:10],
            "challenging": challenging[:10]
        }
    }


def get_time_distribution_stats(user_id, days=30):
    """
    Get the user's time distribution stats
    
    Args:
        user_id (int): The ID of the user
        days (int): Number of days to look back
        
    Returns:
        dict: Dictionary with time distribution stats
    """
    from app import db
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get hour of day distribution
    hour_stats = db.session.query(
        extract('hour', QuizAttempt.created_at).label('hour'),
        func.count().label('count')
    ).filter(
        QuizAttempt.user_id == user_id,
        QuizAttempt.created_at >= start_date
    ).group_by(
        extract('hour', QuizAttempt.created_at)
    ).order_by(
        extract('hour', QuizAttempt.created_at)
    ).all()
    
    # Get day of week distribution
    day_stats = db.session.query(
        extract('dow', QuizAttempt.created_at).label('day'),
        func.count().label('count')
    ).filter(
        QuizAttempt.user_id == user_id,
        QuizAttempt.created_at >= start_date
    ).group_by(
        extract('dow', QuizAttempt.created_at)
    ).order_by(
        extract('dow', QuizAttempt.created_at)
    ).all()
    
    # Convert to arrays for charting
    hours = [0] * 24
    for stat in hour_stats:
        hours[int(stat.hour)] = stat.count
    
    days_of_week = [0] * 7
    day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for stat in day_stats:
        days_of_week[int(stat.day)] = stat.count
    
    return {
        "hours_of_day": {
            "labels": list(range(24)),
            "counts": hours
        },
        "days_of_week": {
            "labels": day_names,
            "counts": days_of_week
        }
    }


def get_learning_speed_stats(user_id, days=30):
    """
    Get stats about the user's learning speed
    
    Args:
        user_id (int): The ID of the user
        days (int): Number of days to look back
        
    Returns:
        dict: Dictionary with learning speed stats
    """
    from app import db
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get average time per question
    avg_time_per_question = db.session.query(
        func.avg(QuizAnswer.time_taken).label('avg_time')
    ).join(
        QuizAttempt, QuizAttempt.id == QuizAnswer.quiz_attempt_id
    ).filter(
        QuizAttempt.user_id == user_id,
        QuizAttempt.created_at >= start_date
    ).scalar() or 0
    
    # Get average time for correct answers vs incorrect answers
    correct_vs_incorrect = db.session.query(
        QuizAnswer.is_correct,
        func.avg(QuizAnswer.time_taken).label('avg_time'),
        func.count().label('count')
    ).join(
        QuizAttempt, QuizAttempt.id == QuizAnswer.quiz_attempt_id
    ).filter(
        QuizAttempt.user_id == user_id,
        QuizAttempt.created_at >= start_date
    ).group_by(
        QuizAnswer.is_correct
    ).all()
    
    # Get time trend over attempts
    time_trend = db.session.query(
        func.row_number().over(
            order_by=QuizAttempt.created_at
        ).label('attempt_number'),
        func.avg(QuizAttempt.time_taken / QuizAttempt.question_count).label('avg_time_per_question')
    ).filter(
        QuizAttempt.user_id == user_id,
        QuizAttempt.created_at >= start_date
    ).group_by(
        QuizAttempt.id, 
        QuizAttempt.time_taken, 
        QuizAttempt.question_count,
        QuizAttempt.created_at
    ).order_by(
        QuizAttempt.created_at
    ).limit(30).all()
    
    # Process correct vs incorrect data
    correct_time = None
    incorrect_time = None
    correct_count = 0
    incorrect_count = 0
    
    for stat in correct_vs_incorrect:
        if stat.is_correct:
            correct_time = round(stat.avg_time, 2)
            correct_count = stat.count
        else:
            incorrect_time = round(stat.avg_time, 2)
            incorrect_count = stat.count
    
    # Process time trend data
    time_trend_data = {
        "attempt_numbers": [],
        "avg_times": []
    }
    
    for stat in time_trend:
        time_trend_data["attempt_numbers"].append(stat.attempt_number)
        time_trend_data["avg_times"].append(round(stat.avg_time_per_question, 2))
    
    return {
        "overall_avg_time": round(avg_time_per_question, 2),
        "correct_vs_incorrect": {
            "correct": {
                "avg_time": correct_time,
                "count": correct_count
            },
            "incorrect": {
                "avg_time": incorrect_time,
                "count": incorrect_count
            }
        },
        "time_trend": time_trend_data
    }
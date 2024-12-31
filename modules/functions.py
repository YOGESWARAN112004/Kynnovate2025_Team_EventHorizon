from modules import app
import secrets
import os
from datetime import datetime
from modules import db
from modules.modals import User_mgmt

def save_profile_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Images/Users/profile_pics', picture_fn)
    form_pic.save(picture_path)
    return picture_fn

def save_bg_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Images/Users/bg_pics', picture_fn)
    form_pic.save(picture_path)
    return picture_fn

def delete_old_images(image, bg_image):
    profile_pic_path = os.path.join(app.root_path, 'static/Images/Users/profile_pics', image)
    bg_pic_path = os.path.join(app.root_path, 'static/Images/Users/bg_pics', bg_image)
    if image!='default.jpg' and image!='':
        try:
            os.remove(profile_pic_path)
        except OSError:
            pass
    if bg_image!='default_bg.jpg' and bg_image!='':
        try:
            os.remove(bg_pic_path)
        except OSError:
            pass

def save_tweet_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Images/Tweets', picture_fn)
    form_pic.save(picture_path)
    return picture_fn

def check_and_update_streak(user: User_mgmt):
    """Check if today's login continues the streak or breaks it and update points accordingly."""
    today = datetime.utcnow().date()

    # If today's login is the same as the last login, do nothing
    if user.last_login == today:
        return

    # If the last login was yesterday, increment the streak
    if user.last_login and (today - user.last_login).days == 1:
        user.streak_days += 1
    else:
        # If there's a break in consecutive logins, reset the streak to 1
        user.streak_days = 1
    reset_daily_points(user)

    # Update user points based on the streak
    update_points(user)

    # Update the last login date to today
    user.last_login = today
    db.session.commit()

def update_points(user):
    """Update user points based on streak and level without exceeding the daily limit."""
    # Define daily point limits for levels
    level_limits = {
        1: 60,  # Max 60 points for Level 1
        2: 150  # Max 150 points for Level 2
    }

    # Calculate daily points for the streak
    if user.streak_days < 14:
        daily_points = min(user.streak_days * 3, 50)  # Maximum of 50 points for Level 1
    elif user.streak_days >= 14 and user.streak_days < 30:
        daily_points = min(user.streak_days * 10, 150)  # Maximum of 150 points for Level 2
    else:
        daily_points = 250  # Max points for 30+ days streak

    # Get the daily limit for the user's current level
    max_daily_points = level_limits.get(user.level, 60)  # Default to Level 1 limit if level is missing

    # Check if the user's daily points have already reached the limit
    if user.daily_points + daily_points > max_daily_points:
        daily_points = max_daily_points - user.daily_points  # Only add points up to the daily limit

    if daily_points > 0:
        user.points += daily_points  # Add the calculated daily points to total points
        user.daily_points += daily_points  # Track the added points for the day

    # Level up logic
    level_up(user)

    # Commit changes to the database
    db.session.commit()

def level_up(user):
    """Update user level based on points and streak."""
    if user.streak_days >= 14 and user.points >= 2 * 50:
        user.level = 2  # If streak is 2 weeks and max points for that streak
    else:
        user.level = 1  # Default to level 1

    db.session.commit()  # Commit level change

def reset_daily_points():
    """Reset daily points for all users at the start of a new day."""
    users = User_mgmt.query.all()
    for user in users:
        user.daily_points = 0
    db.session.commit()

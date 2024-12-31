Fullstack Social Media Platform
A Flask-based social media platform with a reward engagement system, simulating core Twitter features like post management, retweeting, and profile customization. Users can earn points through interactions, which can be redeemed for rewards like personalization options. The platform also includes secure authentication with flask_login and SQLite for database management.



1. Login and logout functionalities with a login and cookie manager system.
2. Creating own account and update and customize (with setting own profile pictures and image management system).
3. reward points for posting ,commenting, maintaing streak,joining and completing challenges etc..
3. CRUD operations on all your tweets.
4. Retweeting other perople's tweets.
5. Looking up other users profile.


## Database Schema

According to the current functionalities there are 5 tables in the schema. The User has all the info on the user, the Post links the creted posts to their author as:

    User.id --> {author} --> Post.user_id

The Retweets have a different table that the Posts as they point to instances within the Post themselves. Their connection is given as:

    Post.id --> {ori_post} --> Retweet.tweet_id
    User.id --> {retwitter} --> Retweet.user_id

The Timelinr table keeps track of all the posts and the retweets that were created since day zero. Their relationship is given as:

    Post.id --> {from_post} --> Timeline.post_id
    Retweet.id --> {from_retweet} --> Timeline.retweet_id

The Bookmark keeps track of all the posts that the user saves as a bookmark, Their relationship is given as :

    Post.id --> {saved_post} --> Bookmark.post_id
    User.id --> {saved_by} --> Bookmark.user_id

__NOTE :__ This portion is yet to be implemented
The Bookmark Table joins the User table with the Posts that the user saves. Relationship given as:

    User.id --> {by_user} --> Bookmark.user_id
    Post.id --> {saved_post} --> Bookmark.post_id

The complete schema structure is given below:

## Note

1. The database has been built on SQLite browser using SQLAlchemy so is not currently scalabe. But due to Flask's upwards compatibility, can be shifted to PostgreSQL whenever needed.
2. The login management system hashshes the passwords and follows a strict cookie management and uses flask_login_manager to time the user sessions and hence provides intermediate level of protection.
3. Built using a virtual environmen so can be easily downloaded and run on your local machine.

### To run on your machine

1. Clone this repo git clone https://github.com/YOGESWARAN112004/Kynnovate2025_Team_EventHorizon.git

2. Install Dependencies
   ```
   pip install -r requirements.txt
   ```
3. Run the application
   ```
   python run.py
   ```

### Test User Credentials
login credentials or u can create a new account

1. Username : yogesh
2. Email : 12147yogeshwaransnm@gmail.com
3. Password : 123456



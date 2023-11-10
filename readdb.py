from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from app import db

def confirm_user_pass(name, password):
    result = db.session.execute(text("SELECT passwords FROM users WHERE names=:name"), {"name":name})
    user_pass = result.fetchone()
    if user_pass == None:
        return False
    return check_password_hash(user_pass[0], password)

def get_areas():
    result = db.session.execute(text("SELECT id, names FROM areas"))
    return result.fetchall()

def get_area_by_id(id):
    result = db.session.execute(text("SELECT id, names FROM areas WHERE id=:id"), {"id": id})
    return result.fetchone()

def get_discussions_by_area(name):
    result = db.session.execute(text("SELECT id, names, area, created_at FROM discussions WHERE area=:name"), {"name": name})
    return result.fetchall()

def get_discussion_by_id(id):
    result = db.session.execute(text("SELECT id, names, area, created_at FROM discussions WHERE id=:id"), {"id": id})
    return result.fetchone()

def get_discussion_by_writer(name):
    result = db.session.execute(text("SELECT id, names, area, starter FROM discussions WHERE starter=:name ORDER BY created_at"), {"name":name})
    return result.fetchall()

def get_messages_from_discussion(name):
    result = db.session.execute(text("SELECT writer, content, discussion, created_at FROM messages WHERE discussion=:name"), {"name": name})
    return result.fetchall()

def get_friends_by_user(name):
    result = db.session.execute(text("SELECT F1.user2 FROM friendlist F1,friendlist F2 WHERE F1.user1=:name AND F1.user1=F2.user2 AND F1.user2=F2.user1"), {"name":name})
    return result.fetchall()

def get_friend_requests(name):
    requests = []
    result = db.session.execute(text("SELECT user1, user2 FROM friendlist WHERE user2=:name"), {"name":name})
    potential = result.fetchall()
    friends = get_friends_by_user(name)
    for user in potential:
        if user not in friends:
            requests.append(user)
    return friends

def is_admin(name):
    result = db.session.execute(text("SELECT admin FROM users WHERE names=:name"), {"name":name})
    return result.fetchone()[0]
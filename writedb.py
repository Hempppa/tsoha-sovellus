from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from app import db

def add_area(name):
    db.session.execute(text("INSERT INTO areas (names) VALUES (:name)"), {"name":name})
    db.session.commit()

def add_discussion(name, area):
    db.session.execute(text("INSERT INTO discussions (names, area) VALUES (:name, :area)"), {"name":name, "area": area})
    db.session.commit()

def add_message(writer, content, discussion):
    db.session.execute(text("INSERT INTO messages (writer, content, discussion, created_at) VALUES (:writer, :content, :discussion, NOW())"), {"name":writer, "content":content, "discussion":discussion})
    db.session.commit()

def add_user(user, password):
    new_pass = generate_password_hash(password)
    db.session.execute(text("INSERT INTO users (names, passwords) VALUES (:name, :password)"), {"name":user, "password":new_pass})
    db.session.commit()

def change_user_pass(user, password):
    new_pass = generate_password_hash(password)
    db.session.execute(text("UPDATE users SET passwords=:password WHERE names=:name"), {"name":user, "password":new_pass})
    db.session.commit()

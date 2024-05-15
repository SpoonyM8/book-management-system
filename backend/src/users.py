import sqlite3
from uuid import uuid4

from ..config import db
from .error import InputError, DatabaseError
from re import match
from .constant import email_pattern, password_pattern
from .helper import generate_token
from .collections import create_collection

def register(json):
    try:
        username = json["username"]
        firstName = json["firstName"]
        lastName = json["lastName"]
        email = json["email"]
        password = json["password"]
    except KeyError:
        raise InputError(description="missing user data")
    
    if len(username) > 50 or len(firstName) > 50 or len(lastName) > 50 or len(email) > 50 or len(password) > 30:
        raise InputError(description="field too long")

    if not match(email_pattern, email):
        raise InputError(description="email is invalid")

    if not match(password_pattern, password):
        raise InputError(description="password is invalid")

    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
         
        cur.execute(f"""select * from Users where username="{username}";""")
        if len(cur.fetchall()) != 0:
            raise InputError("username already exists")

        cur.execute(f"""select * from users where email="{email}";""")
        if len(cur.fetchall()) != 0:
            raise InputError("email already exists")

        cur.execute(f"""insert into Users values ("{username}", "{firstName}", "{lastName}", "{email}", "{password}");""")
        conn.commit()

        ##cur.execute(f"""insert into Collections values ("{str(uuid4())}", "{username}", "main");""")
        create_collection(username, "main")
        conn.commit()

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        conn.close()

    return {"token": generate_token(username)}

def login(json):
    if "password" not in json.keys():
        raise InputError("missing password data")

    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        if "username" not in json.keys() and "email" not in json.keys():
            raise InputError("missing login data")

        field = "username" if "username" in json.keys() else "email"
        cur.execute(f"""select userPassword, username from Users where {field}="{json[field]}";""")
        tuples = cur.fetchone()
        
        if not tuples:
            raise InputError("logins details do not exist")
        
        if tuples[0] != json["password"]:
            raise InputError("incorrect password")

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        conn.close()

    return {"token": generate_token(tuples[1])}
        
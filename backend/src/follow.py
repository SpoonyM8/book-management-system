import sqlite3
from ..config import db
from .error import InputError, DatabaseError, AccessError

def user_exists(username):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
    
        cur.execute(f"""select * from Users where username="{username}";""")
        tuple = cur.fetchone()
        if not tuple:
            raise InputError("user does not exist to follow")

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def already_following(username1, username2):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
    
        cur.execute(f"""select * from Follows where username1="{username1}" and username2="{username2}";""")
        tuple = cur.fetchone()
        if not tuple:
            return False

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return True

def follow(username1, username2):
    if username1 == username2:
        raise InputError("cannot follow yourself")
    
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
    
        user_exists(username2)
        if already_following(username1, username2):
            raise InputError("already following user")

        cur.execute(f"""insert into Follows values ("{username1}", "{username2}");""")
        conn.commit()

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def unfollow(username1, username2):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
    
        user_exists(username2)
        if not already_following(username1, username2):
            raise AccessError("not already following user")

        cur.execute(f"""delete from Follows where username1="{username1}" and username2="{username2}";""")
        conn.commit()

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def followers(username):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
    
        user_exists(username)
        cur.execute(f"""select username1 from Follows where username2="{username}";""")
        tuples = cur.fetchall()
        followers = []
        for tuple in tuples:
            followers.append(tuple[0])

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return {"followers": followers}

def following(username):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        user_exists(username)
        cur.execute(f"""select username2 from Follows where username1="{username}";""")
        tuples = cur.fetchall()
        following = []
        for tuple in tuples:
            following.append(tuple[0])

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return {"following": following} 
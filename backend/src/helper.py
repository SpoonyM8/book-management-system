from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt
from datetime import timedelta, datetime, timezone
from functools import wraps
from ..config import db
from .error import UnauthorizedError, DatabaseError
import sqlite3


def generate_token(username):
    return create_access_token(identity=username, expires_delta=timedelta(hours=1))

def check_jwt():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            # first check if its expired
            if claims["exp"] <= datetime.timestamp(datetime.now(timezone.utc)):
                raise UnauthorizedError(description="token has expired")
            
            # then check if user in subject exists
            username = claims["sub"]
            try:
                conn = sqlite3.connect(db)
                cur = conn.cursor()

                cur.execute(f"""select username from Users where username="{username}";""")

                if cur.fetchone() is None:
                    raise UnauthorizedError(description="Invalid JWT, no matching user")
            except sqlite3.Error:
                raise DatabaseError(description="database error")
            finally:
                cur.close()
                conn.close()

            return fn(*args, **kwargs)
        return decorator
    return wrapper

            

            



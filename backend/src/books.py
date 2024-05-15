import sqlite3
from ..config import db
from json import dumps
from .error import InputError, DatabaseError

def details(bookID):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        cur.execute(f"""select * from Books where bookID="{bookID}";""")
        tuples = cur.fetchone()
        if not tuples:
            raise InputError("bookID does not exist")

        details = {}
        details["bookID"] = tuples[0]
        details["title"] = tuples[1]
        details["author"] = tuples[2]
        details["yearPublished"] = tuples[3]
        details["publisher"] = tuples[4]
        details["coverImage"] = tuples[5]
        details["numRead"] = tuples[6]
        details["averageRating"] = tuples[7]
        details["numRatings"] = tuples[8]
        details["genre"] = tuples[9]

        cur.execute(f"""select * from Reviews where bookID="{bookID}";""")
        tuples = cur.fetchall()
        reviews = []
        for tuple in tuples:
            reviews.append({
                "username": tuple[0],
                "rating": int(tuple[2]),
                "comment": tuple[3]
            })
        details["reviews"] = dumps(reviews)

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        conn.close()

    return details


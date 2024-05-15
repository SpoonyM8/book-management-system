import sqlite3
from ..config import db
from .error import InputError, AccessError, DatabaseError
from datetime import datetime

def added_to_personal(bookID, username):
    hasRead = False
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select collectionID from Collections where username="{username}";""")
        collectionIDs = cur.fetchall()
        for collectionID in collectionIDs:
            cur.execute(f"""select bookID from CollectionBooks where collectionID="{collectionID[0]}";""")
            readBookIDs = cur.fetchall()
            for readBookID in readBookIDs:
                if readBookID[0] == bookID:
                    hasRead = True
                    break
            if hasRead:
                break
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return hasRead

def added_to_shared(bookID, username):
    hasRead = False
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select collectionID from SharedCollectionMembers where member="{username}";""")
        collectionIDs = cur.fetchall()
        for collectionID in collectionIDs:
            cur.execute(f"""select bookID from SharedCollectionBooks where collectionID="{collectionID[0]}" and member="{username}";""")
            readBookIDs = cur.fetchall()
            for readBookID in readBookIDs:
                if readBookID[0] == bookID:
                    hasRead = True
                    break
            if hasRead:
                break
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return hasRead

def add_review(username, bookID, reqJson):
    if "rating" not in reqJson.keys():
        raise InputError("reviews must have a rating")

    if int(reqJson["rating"]) < 0 or int(reqJson["rating"]) > 5:
        raise InputError("rating is outside of range")

    if reqJson.get("comment") and len(reqJson["comment"]) > 1000:
        raise InputError("comment is exceeds limit")

    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select * from Books where bookID="{bookID}";""")
        tuples = cur.fetchone()
        if not tuples:
            raise InputError("bookID does not exist")
 
        cur.execute(f"""select * from Reviews where bookID="{bookID}" and username="{username}";""")
        tuples = cur.fetchone()
        if tuples:
            raise AccessError("already reviewed book")

        if not added_to_personal(bookID, username) and not added_to_shared(bookID, username):
            raise AccessError("user must read book before reviewing")

        now = datetime.now()
        if not reqJson.get("comment"):
            cur.execute(f"""insert into Reviews (username, bookID, rating, timeAdded) values ("{username}","{bookID}",{int(reqJson["rating"])},"{now}");""")
        else:
            cur.execute(f"""insert into Reviews values ("{username}","{bookID}",{int(reqJson["rating"])},"{reqJson["comment"]}","{now}");""")
        conn.commit()

        cur.execute(f"""select * from Books where bookID="{bookID}";""")
        tuples = cur.fetchone()
        update_added(bookID, float(tuples[7]), int(reqJson["rating"]), int(tuples[8]))

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def delete_review(username, bookID):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select * from Reviews where username="{username}" and bookID="{bookID}";""")
        tuples = cur.fetchone()
        if not tuples:
            raise AccessError("review does not exist")

        rating  = tuples[2]
        cur.execute(f"""delete from Reviews where username="{username}" and bookID="{bookID}";""")
        conn.commit()

        cur.execute(f"""select * from Books where bookID="{bookID}";""")
        tuples = cur.fetchone()
        update_deleted(bookID, float(tuples[7]), rating, int(tuples[8]))

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def update_added(bookID, currAvg, rating, n):
    newAvg = (currAvg * n) / (n + 1) + rating / (n + 1)
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""update Books set averageRating={newAvg}, numRatings={n+1} where bookID="{bookID}";""")
        conn.commit()
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def update_deleted(bookID, currAvg, rating, n):
    if n - 1 == 0:
        newAvg = 0
    else :
        newAvg = (currAvg * n - rating) / (n - 1)
    
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""update Books set averageRating={newAvg}, numRatings={n-1} where bookID="{bookID}";""")
        conn.commit()
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def get_reviews(bookID):
    reviews = []
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select * from Reviews
where bookID="{bookID}"
order by timeAdded desc;""")
        tuples = cur.fetchall()
        for tuple in tuples:
            review = {}
            review["username"] = tuple[0]
            review["rating"] = tuple[2]
            if tuple[3] != None:
                review["comment"] = tuple[3]
            else:
                review["comment"] = ""
            review["timeAdded"] = tuple[4]
            reviews.append(review)

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return {"reviews": reviews}
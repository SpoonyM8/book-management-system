import sqlite3
from ..config import db

def clear():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    q = """delete from UserGoals;
delete from hasRead;
delete from Users;
delete from Reviews;
delete from Collections;
delete from CollectionBooks;
delete from SharedCollectionBooks;
delete from SharedCollectionMembers;
delete from SharedCollections;
delete from Follows;
update Books set averageRating=0.0, numRead=0, numRatings=0;"""
    cur.executescript(q)
    conn.commit()

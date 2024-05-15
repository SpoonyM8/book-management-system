import sqlite3
import datetime
from .goals import update_monthly_goal
from uuid import uuid4
from ..config import db
from .error import InputError, AccessError, DatabaseError

####### Helpers

def get_collection_name(collectionID):
    name = ""
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select collectionName from Collections where collectionID="{collectionID}";""")
        name = cur.fetchone()[0]
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return name

def book_exists(bookID, collectionID):
    exists = False
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select * from CollectionBooks where collectionID="{collectionID}" 
                                and bookID="{bookID}";""")
        if cur.fetchone():
            exists = True
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return exists

def collection_exists(username, collectionName):
    exists = False
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select * from Collections where collectionName="{collectionName}" 
                            and username="{username}";""")
        if cur.fetchone():
            exists = True
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return exists

def increase_reads(bookID):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select numRead from Books where bookID="{bookID}";""")
        newNumRead = int(cur.fetchone()[0]) + 1
        cur.execute(f"""update Books set numRead="{newNumRead}"
                                where bookId="{bookID}";""")
        conn.commit()
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def book_read(username, bookID): # boolean finds if book has already been read by user
    read = False
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""
                select * from hasRead where username="{username}" 
                    and bookID="{bookID}";
        """)
        if cur.fetchone():
            read = True
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()  
    return read

def update_user_books_read(username, bookID):
    timeNow = datetime.datetime.now()
    currMonth = timeNow.month
    currYear = timeNow.year
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        newRead = True
        if book_read(username, bookID):   
            newRead = False
        else:
            cur.execute(f"""
                    insert into hasRead values ("{username}", "{bookID}", "{currMonth}", "{currYear}");
            """)
            conn.commit()
            update_monthly_goal(username)  
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return newRead

def getUsername(collectionID):
    username = ""
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select username from Collections where collectionID="{collectionID}";""")
        username = cur.fetchone()[0]
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close() 
    return username

#### Main Functions

def create_collection(username, collectionName):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        if collection_exists(username, collectionName):
            raise InputError("Collection name already exists")
        collectionID = str(uuid4())
        cur.execute(f"""
                insert into Collections values ("{collectionID}", "{username}", "{collectionName}");
        """)
        conn.commit()   
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    return {"collectionID": collectionID}


def add_book_to_collection(bookID, collectionID):
    try: 
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        collectionName = get_collection_name(collectionID)

        if book_exists(bookID, collectionID):
            raise InputError(f"Collection '{collectionName}' already includes this book")
        cur.execute(f"""
                insert into CollectionBooks values ("{bookID}", "{collectionID}", "{datetime.datetime.now()}");
        """)
        conn.commit()
        ## update hasRead sql table, subsequently update current monthly goal
        if update_user_books_read(getUsername(collectionID), bookID):
            # update numRead for book 
            increase_reads(bookID)
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()   
            
def remove_book_from_collection(bookID, collectionID):
    try: 
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        collectionName = get_collection_name(collectionID)

        if not book_exists(bookID, collectionID):
            raise InputError(f"Collection '{collectionName}' does not include this book")
        cur.execute(f"""delete from CollectionBooks where collectionID="{collectionID}" 
                            and bookID="{bookID}";
        """)
        conn.commit()
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def get_collections(username):
    # returns top ten recently added books for each collection with basic book details
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        collectionsList = []
        cur.execute(f"""select collectionID, collectionName from Collections where username="{username}";""")
        collections = cur.fetchall()
        for collection in collections:
            cur.execute(f"""select b.bookID, b.title, b.coverImage, b.author from Books b
                                join CollectionBooks cb on cb.bookID = b.bookID
                                where cb.collectionID="{collection[0]}"
                                order by cb.timeAdded desc;""")
            books = cur.fetchall()
            collectionDetails = {
                "collectionID": collection[0],
                "collectionName": collection[1],
                "numBooks": len(books),
                "books": books[:10] # List of dictionary [[bookID, title, coverImage]]
            }
            collectionsList.append(collectionDetails)
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close() 
    return {"collections": collectionsList} # List of dictionaries (collectionDetails)


def get_collection_details(collectionID):
    #return book's title, author(s), publisher, publication date, category
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select b.bookID, b.title, b.author, b.yearPublished, b.coverImage, b.genre from Books b
                            join CollectionBooks cb on (b.bookID == cb.bookID)
                            where collectionID="{collectionID}";""")
        books = cur.fetchall() # [bookID, title, author, yearPubilshed, coverImage, genre]   
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close() 
    return {"books": books} # List of list (books)

def delete_collection(username, collectionID):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select username, collectionName from Collections where collectionID="{collectionID}";""")   
        tuple = cur.fetchone()
        if not tuple:
            raise InputError("collection does not exist")
        if tuple[0] != username:
            raise AccessError("user is not collection owner")
        if tuple[1] == "main":
            raise AccessError("cannot delete main collection")

        cur.executescript(f"""
delete from Collections where collectionID="{collectionID}";
delete from CollectionBooks where collectionID="{collectionID}";""")
        conn.commit()
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()



import sqlite3
from uuid import uuid4
from ..config import db
from .error import InputError, AccessError, DatabaseError
from datetime import datetime
from .collections import update_user_books_read, increase_reads

################################################################################
### HELPERS

def shared_collection_exists(collectionID):
    exists = True
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        cur.execute(f"""select * from SharedCollections where collectionID="{collectionID}";""")
        tuple = cur.fetchone()
        if not tuple:
            exists = False

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return exists

def is_member(collectionID, username):
    member = True
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        cur.execute(f"""select * from SharedCollectionMembers where collectionID="{collectionID}" and member="{username}";""")
        tuple = cur.fetchone()
        if not tuple:
            member = False

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return member

def is_owner(collectionID, username):
    owner = True
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        cur.execute(f"""select * from SharedCollections where collectionID="{collectionID}" and collectionOwner="{username}";""")
        tuple = cur.fetchone()
        if not tuple:
            owner = False

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return owner

################################################################################
### MAIN FUNCTIONS

def create_shared_collection(username, collectionName):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        cur.execute(f"""select * from SharedCollections where collectionName="{collectionName}" and collectionOwner="{username}";""")
        tuple = cur.fetchone()
        if tuple:
            raise InputError("shared collection with given name exists for owner")

        collectionID = str(uuid4())
        cur.executescript(f"""
insert into SharedCollections values ("{collectionID}", "{collectionName}", "{username}");
insert into SharedCollectionMembers values ("{collectionID}", "{username}");
""")
        conn.commit()

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return {"collectionID": collectionID}

def delete_shared_collection(username, collectionID):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        if not shared_collection_exists(collectionID):
            raise InputError("shared collection does not exist")

        if not is_owner(collectionID, username):
            raise AccessError("user is not owner of shared collection")

        cur.executescript(f"""
delete from SharedCollections where collectionID="{collectionID}";
delete from SharedCollectionMembers where collectionID="{collectionID}";
delete from SharedCollectionBooks where collectionID="{collectionID}";
""")
        conn.commit()

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def join_shared_collection(username, collectionID):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        if not shared_collection_exists(collectionID):
            raise InputError("shared collection does not exist")

        if is_member(collectionID, username):
            raise AccessError("user already member of shared collection")

        cur.execute(f"""insert into SharedCollectionMembers values ("{collectionID}", "{username}");""")
        conn.commit()

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def leave_shared_collection(username, collectionID):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        if not shared_collection_exists(collectionID):
            raise InputError("shared collection does not exist")
        
        if is_owner(collectionID, username):
            raise AccessError("user is owner of shared collection")

        if not is_member(collectionID, username):
            raise AccessError("user not member of shared collection")

        cur.executescript(f"""
delete from SharedCollectionMembers where collectionID="{collectionID}" and member="{username}";
delete from SharedCollectionBooks where collectionID="{collectionID}" and member="{username}";
""")
        conn.commit()

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def add_book_shared_collection(username, collectionID, bookID):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        if not shared_collection_exists(collectionID):
            raise InputError("shared collection does not exist")

        if not is_member(collectionID, username):
            raise AccessError("user not member of shared collection")

        cur.execute(f"""select * from SharedCollectionBooks where collectionID="{collectionID}" and bookID="{bookID}" and member="{username}";""")
        tuple = cur.fetchone()
        if tuple:
            raise InputError("book already added to collection by user")

        cur.execute(f"""insert into SharedCollectionBooks values ("{bookID}", "{collectionID}", "{username}", "{datetime.now()}");""")
        ## update hasRead sql table, subsequently update current monthly goal
        conn.commit()
        if update_user_books_read(username, bookID):
            ## update numRead for book
            increase_reads(bookID)
    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def remove_book_shared_collection(username, collectionID, bookID):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        if not shared_collection_exists(collectionID):
            raise InputError("shared collection does not exist")

        if not is_member(collectionID, username):
            raise AccessError("user not member of shared collection")

        cur.execute(f"""select * from SharedCollectionBooks where collectionID="{collectionID}" and bookID="{bookID}" and member="{username}";""")
        tuple = cur.fetchone()
        if not tuple:
            raise InputError("book has not been added to collection by user")

        cur.execute(f"""delete from SharedCollectionBooks where collectionID="{collectionID}" and bookID="{bookID}" and member="{username}";""")
        conn.commit()

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

def shared_collection_details(username, collectionID):
    details = {}
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        if not shared_collection_exists(collectionID):
            raise InputError("shared collection does not exist")

        #if not is_member(collectionID, username):
            #raise AccessError("user not member of shared collection")

        cur.execute(f"""select * from SharedCollections where collectionID="{collectionID}";""")
        tuple = cur.fetchone()
        details["collectionName"] = tuple[1]
        details["owner"] = tuple[2]

        cur.execute(f"""select count(*) from SharedCollectionMembers where collectionID="{collectionID}";""")
        details["numMembers"] = int(cur.fetchone()[0])

        cur.execute(f"""select distinct bookID from SharedCollectionBooks where collectionID="{collectionID}";""")
        details["numBooks"] = len(cur.fetchall())
        
        details["books"] = [] 
        cur.execute(f"""select * from SharedCollectionBooks where collectionID="{collectionID}";""")
        tuples = cur.fetchall()
        searched = []
        for tuple in tuples:
            bookInfo = {}
            if tuple[0] in searched:
                continue
            
            cur.execute(f"""select * from Books where bookID="{tuple[0]}";""")
            info = cur.fetchone()
            bookInfo["bookID"] = info[0]
            bookInfo["title"] = info[1]
            bookInfo["author"] = info[2]
            bookInfo["yearPublished"] = info[3]
            bookInfo["publisher"] = info[4]
            bookInfo["coverImage"] = info[5]
            bookInfo["numRead"] = info[6]
            bookInfo["averageRating"] = info[7]
            bookInfo["numRatings"] = info[8]
            bookInfo["genre"] = info[9]

            cur.execute(f"""select count(*) from SharedCollectionBooks where bookID="{tuple[0]}" and collectionID="{collectionID}";""")
            bookInfo["numRead"] = int(cur.fetchone()[0])

            details["books"].append(bookInfo)
            searched.append(tuple[0])

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return details

def shared_collection(username):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"""select collectionID from SharedCollectionMembers where member="{username}";""")
        
        tuples1 = cur.fetchall()
        collections = []
        for tuple1 in tuples1:
            collection = {}
            collection["collectionID"] = tuple1[0]
            cur.execute(f"""select * from SharedCollections where collectionID="{tuple1[0]}";""")
            
            tuple2 = cur.fetchone()
            collection["collectionName"] = tuple2[1]
            collection["isOwner"] = username == tuple2[2] 
            
            cur.execute(f"""select count(distinct bookID) from SharedCollectionBooks where collectionID="{tuple1[0]}";""")
            collection["numBooks"] = cur.fetchone()[0]
            
            cur.execute(f"""select distinct s.bookID, b.title, b.coverImage, b.author from SharedCollectionBooks s 
inner join Books b on b.bookID=s.bookID
where s.collectionID="{tuple1[0]}"
order by s.timeAdded desc 
limit 10;""")
            collection["books"] = cur.fetchall()
            
            collections.append(collection)

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return {"collections": collections}

def shared_collection_username(username):
    return shared_collection(username)

def shared_collection_is_member(collectionID, username):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        
        cur.execute(f"""select * from SharedCollectionMembers
where collectionID = "{collectionID}"
and member = "{username}";""")
        is_member = cur.fetchone() != None

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return {"is_member": is_member}

def shared_collection_all(username):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()    
        cur.execute(f"""select * from SharedCollections;""")
        
        tuples1 = cur.fetchall()
        collections = []


        for tuple1 in tuples1:
            collection = {}
            collection["collectionID"] = tuple1[0]
            collection["collectionName"] = tuple1[1]
            collection["isOwner"] = username == tuple1[2]
            
            cur.execute(f"""select count(distinct bookID) from SharedCollectionBooks where collectionID="{tuple1[0]}";""")
            collection["numBooks"] = cur.fetchone()[0]
            
            cur.execute(f"""select distinct s.bookID, b.title, b.coverImage, b.author from SharedCollectionBooks s 
inner join Books b on b.bookID=s.bookID
where s.collectionID="{tuple1[0]}"
order by s.timeAdded desc 
limit 10;""")
            collection["books"] = cur.fetchall()
            
            collections.append(collection)

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return {"collections": collections} 
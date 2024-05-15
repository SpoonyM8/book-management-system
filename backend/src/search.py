import sqlite3
import json
from ..config import db
from .error import InputError, DatabaseError

def search(reqJson):
  title = reqJson.get("title")
  author = reqJson.get("author")
  username = reqJson.get("username")

  try:
    if not title and not author and not username:
      raise InputError(description="No search parameters in request")

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    if title or author:
      res = searchForBook(title, author, cur)
    else:
      res = searchForUser(username, cur)
    
  except sqlite3.Error:
    raise DatabaseError(description="database error")
  finally:

    if not res:
      raise InputError(description="No matches found")
    cur.close()
    conn.close()
  
  return res

def searchForBook(title, author, cur):
  if title and author:
    cur.execute(f"""select * from Books where title like '%{title}%' and author like '%{author}%';""" )
  elif title:
    cur.execute(f"""select * from Books where title like '%{title}%';""")
  else:
    cur.execute(f"""select * from Books where author like '%{author}%';""")
  queryRes = cur.fetchall()
  res = list()
  for book in queryRes:
    d = dict()
    d["bookId"] = book[0]
    d["title"] = book[1]
    d["author"] = book[2]
    d["yearPublished"] = book[3]
    d["publisher"] = book[4]
    d["coverImage"] = book[5]
    d["numRead"] = book[6]
    d["averageRating"] = book[7]
    d["numRatings"] = book[8]
    d["genre"] = book[9]
    res.append(d)

  return res

def searchForUser(username, cur):
  cur.execute(f"""select username from Users where username like '%{username}%';""")
  queryRes = cur.fetchall()
  res = list()
  for user in queryRes:
    d = dict()
    d["username"] = user[0]
    res.append(d)
  return res

def getDetails(bookID):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
         
        cur.execute(f"""select * from Books where bookID="{bookID}";""")
        tuples = cur.fetchone()

        if not tuples:
            raise InputError("bookID does not exist")

    except sqlite3.Error:
        raise DatabaseError(description="database error")
    finally:
        conn.close()

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

    return details


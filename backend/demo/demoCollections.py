import requests
import sqlite3
from ..config import url, db

# Ben #######################################################################

requests.delete(f"{url}/clear")


def getHarryBookData():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f"select * from books where title like 'harry%' limit 11;")
    bookData = cur.fetchall()
    cur.close()
    conn.close()
    return bookData

def getStineBookData():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f"select * from books where author like 'R.L.%' limit 15;")
    bookData = cur.fetchall()
    cur.close()
    conn.close()
    return bookData



StineBooks = getStineBookData()
Harrybooks = getHarryBookData() 

user1 = {
        "username": "Hjones45",
        "firstName": "Herb",
        "lastName": "Jones",
        "email": "notonHerb@nba.com",
        "password": "Nooooooo2$"
    }
user2 = {
        "username": "jHarden23",
        "firstName": "James",
        "lastName": "Harden",
        "email": "freethrow@nba.com",
        "password": "Waaaaaaa9$"
    }

user3 = {
        "username": "Kingram66",
        "firstName": "Brandon",
        "lastName": "Ingram",
        "email": "slimreaper@nba.com",
        "password": "Booooooo6!"
    }

res = requests.post(f"{url}/register", json=user1)
usrHeader1 = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.post(f"{url}/register", json=user2)
usrHeader2 = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.post(f"{url}/register", json=user3)
usrHeader3 = {
        "Authorization": f"Bearer {res.json()['token']}"
    }

res = requests.post(f"{url}/collections/create/harryP", headers=usrHeader2)
collectionID = res.json()["collectionID"]
for book in Harrybooks:
    res = requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=usrHeader2)

res = requests.post(f"{url}/sharedCollection/create/Stinies", headers=usrHeader3)
collectionID1 = res.json()["collectionID"]
for book in StineBooks:
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{book[0]}", headers=usrHeader3)


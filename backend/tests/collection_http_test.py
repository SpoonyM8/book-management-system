import pytest
import requests
import sqlite3
from json import loads
from ..config import url, db
from ..src.constant import _OK, _InputError, _AccessError

@pytest.fixture
def clear():
    requests.delete(f"{url}/clear")

@pytest.fixture
def tokens():
    users = ["a", "b", "c"]
    tokens = []
    for user in users:
        data = {
            "username": f"{user}",
            "firstName": "b",
            "lastName": "c",
            "email": f"{user}@c.com",
            "password": "aaaaaa1!"
        }
        res = requests.post(f"{url}/register", json=data)
        tokens.append(res.json()["token"])
    return tokens, users

def getBookData():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("select * from books order by random() limit 1;")
    bookData = cur.fetchone()
    cur.close()
    conn.close()
    return bookData

def getBookDataMult():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("select * from books order by random() limit 5;")
    bookData = cur.fetchall()
    cur.close()
    conn.close()
    return bookData  

def getBookDataEleven():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("select * from books order by random() limit 11;")
    bookData = cur.fetchall()
    cur.close()
    conn.close()
    return bookData  

### tests

def test_create_collection(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/collections/create/a", headers=headers)
    assert res.status_code == _OK
    res = requests.post(f"{url}/collections/create/a", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/collections/create/a", headers=headers)
    assert res.status_code == _OK


def test_main_collection_create_add(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()["collections"]
    assert len(resJson) == 1
    collection = resJson[0]
    assert collection["collectionName"] == "main"

    collectionID = collection["collectionID"]
    book = getBookData()
    res = requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=headers)
    assert res.status_code == _OK

    res = requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=headers)
    assert res.status_code == _InputError 


def test_multiple_collection_add(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/collections/create/a", headers=headers)
    assert res.status_code == _OK
    collectionID_0 = res.json()["collectionID"]

    res0 = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/collections/create/b", headers=headers)
    assert res.status_code == _OK
    collectionID_1 = res.json()["collectionID"]

    res1 = requests.get(f"{url}/collections/user/{usernames[1]}", headers=headers)

    assert res0.status_code == _OK and res1.status_code == _OK
    res0Json = res0.json()["collections"]
    res1Json = res1.json()["collections"]

    assert len(res0Json) == 2 and len(res1Json) == 2
    collection_0_name = [res0Json[0]["collectionName"], res0Json[1]["collectionName"]]
    collection_1_name = [res1Json[0]["collectionName"], res1Json[1]["collectionName"]]

    assert collection_0_name[0] == "main" and collection_1_name[0] == "main"
    assert collection_0_name[1] == "a" and collection_1_name[1] == "b"

    collection_0_ID = res0Json[1]["collectionID"]
    collection_1_ID = res1Json[1]["collectionID"]
    assert collection_0_ID == collectionID_0 and collection_1_ID == collectionID_1

    book = getBookData()
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }

    collection_0_ID = res0Json[0]["collectionID"]
    collection_1_ID = res0Json[1]["collectionID"]  
    collection_2_ID = res1Json[1]["collectionID"] 
    res = requests.post(f"{url}/collections/{collection_0_ID}/add/{book[0]}", headers=headers)
    assert res.status_code == _OK
    res = requests.post(f"{url}/collections/{collection_1_ID}/add/{book[0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/collections/{collection_2_ID}/add/{book[0]}", headers=headers)
    assert res.status_code == _OK 


def test_collection_remove(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/collections/create/a", headers=headers)
    collectionID = res.json()["collectionID"]

    book = getBookData()

    res = requests.delete(f"{url}/collections/{collectionID}/remove/{book[0]}", headers=headers)
    assert res.status_code == _InputError

    res = requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=headers)
    assert res.status_code == _OK

    res = requests.delete(f"{url}/collections/{collectionID}/remove/{book[0]}", headers=headers)
    assert res.status_code == _OK 

    res = requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=headers)
    assert res.status_code == _OK


def test_collection_details(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    resJson = res.json()["collections"]
    collectionID = resJson[0]["collectionID"]

    books = getBookDataMult()
    expBookDetails = []
    for book in books:
        res = requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=headers)
        bookDetails = [book[0], book[1], book[2], book[3], book[5], book[9]]
        expBookDetails.append(bookDetails)

    res = requests.get(f"{url}/collections/{collectionID}", headers=headers)
    resBooks = res.json()["books"]
    assert len(resBooks) == 5
    for resBook in resBooks:
        assert resBook in expBookDetails


def test_get_collection_books_recent(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    resJson = res.json()["collections"]
    collectionID = resJson[0]["collectionID"]

    books = getBookDataEleven()
    expBookDetails = []
    for book in books:
        res = requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=headers)
        bookDetails = [book[0], book[1], book[5], book[2]]
        expBookDetails.insert(0, bookDetails)
    expBookDetails.pop()

    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    resCollection = res.json()["collections"][0]
    assert resCollection["numBooks"] == 11
    resBooks = resCollection["books"]
    for i in range(10):
        assert resBooks[i] == expBookDetails[i]

def test_delete_collection(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    resJson = res.json()
    collections = resJson["collections"]
    assert len(collections) == 1

    headers1 = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/collections/delete/{collections[0]['collectionID']}", headers=headers1)
    assert res.status_code == _AccessError

    res = requests.delete(f"{url}/collections/delete/none", headers=headers)
    assert res.status_code == _InputError
    res = requests.delete(f"{url}/collections/delete/{collections[0]['collectionID']}", headers=headers)
    assert res.status_code == _AccessError

    res = requests.post(f"{url}/collections/create/first", headers=headers)
    collectionID = res.json()["collectionID"]
    requests.post(f"{url}/collections/create/second", headers=headers)

    res = requests.delete(f"{url}/collections/delete/{collectionID}", headers=headers)
    assert res.status_code == _OK
    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    resJson = res.json()
    assert len(resJson["collections"]) == 2
    assert resJson["collections"][0]['collectionName'] == 'main' or resJson["collections"][0]['collectionName'] == 'second'
    assert resJson["collections"][1]['collectionName'] == 'main' or resJson["collections"][1]['collectionName'] == 'second'


def test_book_increase_read(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    resJson = res.json()["collections"]
    collectionID = resJson[0]["collectionID"]

    book = getBookData()
    res = requests.get(f"{url}/books/{book[0]}", headers=headers)
    numRead = res.json()["numRead"]
    assert numRead == 0
    res = requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=headers)

    res = requests.get(f"{url}/books/{book[0]}", headers=headers)
    numRead = res.json()["numRead"]
    assert numRead == 1


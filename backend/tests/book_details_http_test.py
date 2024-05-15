import pytest
import requests
import sqlite3
from ..config import url, db
from ..src.constant import _OK, _InputError
from json import loads

@pytest.fixture
def clear():
    requests.delete(f"{url}/clear")

@pytest.fixture
def token1():
    data = {
        "username": "a",
        "firstName": "b",
        "lastName": "c",
        "email": "b@c.com",
        "password": "aaaaaa1!"
    }
    res = requests.post(f"{url}/register", json=data)
    token = res.json()["token"]
    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    collectionID = res.json()["collectionID"]
    return token, collectionID

@pytest.fixture
def token2():
    data = {
        "username": "x",
        "firstName": "y",
        "lastName": "z",
        "email": "y@z.com",
        "password": "aaaaaa2!"
    }
    res = requests.post(f"{url}/register", json=data)
    token = res.json()["token"]
    headers = {
            "Authorization": f"Bearer {token}"
        }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    collectionID = res.json()["collectionID"]
    return token, collectionID

@pytest.fixture
def tokens():
    tokens = []
    collectionIDs = []
    users = ["t","m","n","p","r","i","w","q","e","d"]
    for u in users:
        data = {
            "username": f"{u}",
            "firstName": "y",
            "lastName": "z",
            "email": f"{u}@z.com",
            "password": "aaaaaa2!"
        }
        res = requests.post(f"{url}/register", json=data)
        tokens.append(res.json()["token"])
        headers = {
            "Authorization": f"Bearer {tokens[-1]}"
        }
        res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
        collectionIDs.append(res.json()["collectionID"])
    return tokens, collectionIDs

def compare(a, b):
    epsilon = 0.001
    return abs(a - b) < epsilon

def getBookData():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("select * from books order by random() limit 1;")
    bookData = cur.fetchone()
    cur.close()
    conn.close()
    return bookData

def addToCollection(collectionID, bookID, headers):
    requests.post(f"{url}/sharedCollection/{collectionID}/add/{bookID}", headers=headers)

def test_invalid_bookID(clear, token1):
    token1, collectionID = token1
    bookID = "none"
    headers = {
        "Authorization": f"Bearer {token1}"
    }
    addToCollection(collectionID, bookID, headers)
    res = requests.get(f"{url}/books/{bookID}", headers=headers)
    assert res.status_code == _InputError

def test_valid_bookID(clear, token1):
    token1, collectionID = token1
    bookData = getBookData()
    headers = {
        "Authorization": f"Bearer {token1}"
    }
    addToCollection(collectionID, bookData[0], headers)
    res = requests.get(f"{url}/books/{bookData[0]}", headers=headers)
    assert res.status_code == _OK
    assert len(res.json()) >= 10
    
    resJson = res.json()
    assert resJson["bookID"] == bookData[0]
    assert resJson["title"] == bookData[1]
    assert resJson["author"] == bookData[2]
    assert resJson["yearPublished"] == bookData[3]
    assert resJson["publisher"] == bookData[4]
    assert resJson["coverImage"] == bookData[5]
    assert resJson["numRead"] == 1
    assert resJson["averageRating"] == bookData[7]
    assert resJson["numRatings"] == bookData[8]
    assert resJson["genre"] == bookData[9]
    assert loads(resJson["reviews"]) == []

def test_valid_book_reviews(clear, token1, token2):
    token1, collectionID1 = token1
    token2, collectionID2 = token2
    bookData = getBookData()
    headers1 = {
        "Authorization": f"Bearer {token1}"
    }
    headers2 = {
        "Authorization": f"Bearer {token2}"
    }
    addToCollection(collectionID1, bookData[0], headers1)
    payload = {
        "rating": 4,
        "comment": "i like this"
    }
    res = requests.post(f"{url}/books/{bookData[0]}/review/add", json=payload, headers=headers1)

    res = requests.get(f"{url}/books/{bookData[0]}", headers=headers2)
    assert res.status_code == _OK
    assert len(res.json()) >= 10

    resJson = res.json()
    reviews = loads(resJson["reviews"])
    assert len(reviews) == 1
    assert reviews[0]["rating"] == 4    
    assert reviews[0]["comment"] == "i like this" 
    assert reviews[0]["username"] == "a"

    payload = {
        "rating": 1,
        "comment": "i hate this"
    }
    addToCollection(collectionID2, bookData[0], headers2)
    res = requests.post(f"{url}/books/{bookData[0]}/review/add", json=payload, headers=headers2)
    
    res = requests.get(f"{url}/books/{bookData[0]}", headers=headers1)
    assert res.status_code == _OK
    assert len(res.json()) >= 10

    resJson = res.json()
    reviews = loads(resJson["reviews"])
    assert len(reviews) == 2
    assert reviews[0]["rating"] == 4    
    assert reviews[0]["comment"] == "i like this"
    assert reviews[0]["username"] == "a"
    assert reviews[1]["rating"] == 1  
    assert reviews[1]["comment"] == "i hate this"
    assert reviews[1]["username"] == "x"

def test_deleted_reviews(clear, token1, token2):
    token1, collectionID1 = token1
    token2, collectionID2 = token2
    bookData = getBookData()
    headers1 = {
        "Authorization": f"Bearer {token1}"
    }
    headers2 = {
        "Authorization": f"Bearer {token2}"
    }

    payload = {
        "rating": 4,
        "comment": "i like this"
    }
    addToCollection(collectionID1, bookData[0], headers1)
    requests.post(f"{url}/books/{bookData[0]}/review/add", json=payload, headers=headers1)

    payload = {
        "rating": 1,
        "comment": "i hate this"
    }
    addToCollection(collectionID2, bookData[0], headers2)
    requests.post(f"{url}/books/{bookData[0]}/review/add", json=payload, headers=headers2)
    res = requests.get(f"{url}/books/{bookData[0]}", headers=headers1)

    resJson = res.json()
    reviews = loads(resJson["reviews"])
    assert len(reviews) == 2
    assert reviews[0]["rating"] == 4    
    assert reviews[0]["comment"] == "i like this"
    assert reviews[0]["username"] == "a"
    assert reviews[1]["rating"] == 1  
    assert reviews[1]["comment"] == "i hate this"
    assert reviews[1]["username"] == "x"

    requests.delete(f"{url}/books/{bookData[0]}/review/delete", headers=headers1)
    res = requests.get(f"{url}/books/{bookData[0]}", headers=headers1)
    
    resJson = res.json()
    reviews = loads(resJson["reviews"])
    assert len(reviews) == 1
    assert reviews[0]["rating"] == 1  
    assert reviews[0]["comment"] == "i hate this"
    assert reviews[0]["username"] == "x"

    requests.delete(f"{url}/books/{bookData[0]}/review/delete", headers=headers2)
    res = requests.get(f"{url}/books/{bookData[0]}", headers=headers2)

    resJson = res.json()
    reviews = loads(resJson["reviews"])
    assert len(reviews) == 0


def test_returned_ratings(clear, tokens):
    tokens, collectionIDs = tokens
    bookData = getBookData()
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/books/{bookData[0]}", headers=headers)
    resJson = res.json()
    assert float(resJson["averageRating"]) == 0.0
    assert int(resJson["numRatings"]) == 0

    ratings = [4,1,3,3,0,2,5,5,2,3]
    for i in range(10):
        headers = {
            "Authorization": f"Bearer {tokens[i]}"
        }
        payload = {
            "rating": ratings[i],
        }
        addToCollection(collectionIDs[i], bookData[0], headers)
        requests.post(f"{url}/books/{bookData[0]}/review/add", json=payload, headers=headers)
        print(i)

        res = requests.get(f"{url}/books/{bookData[0]}", headers=headers)
        resJson = res.json()
        expectedAvg = sum(ratings[0:i+1]) / (i + 1)
        assert compare(float(resJson["averageRating"]), expectedAvg)
        assert int(resJson["numRatings"]) == i + 1

    remove = [3,6,0,2,9,8,7,1,4,5]
    expectedAvg = [2.7778,2.5,2.2857,2.1667,2,2,1,1,2,0]
    for i in range(10):
        headers = {
            "Authorization": f"Bearer {tokens[remove[i]]}"
        }
        requests.delete(f"{url}/books/{bookData[0]}/review/delete", json=payload, headers=headers)

        res = requests.get(f"{url}/books/{bookData[0]}", headers=headers)
        resJson = res.json()
        assert compare(float(resJson["averageRating"]), expectedAvg[i])
        assert int(resJson["numRatings"]) == 10 - i - 1


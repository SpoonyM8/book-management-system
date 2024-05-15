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
def tokens():
    users = ["a", "b", "c", "d", "e"]
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
    return tokens

def getBookDataMult():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("select * from books order by random() limit 10;")
    bookData = cur.fetchall()
    cur.close()
    conn.close()
    return bookData

def test_no_reviews_all(clear, tokens):
    bookDataMult = getBookDataMult()
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    data = {
        "follows": False,
        "genre": False,
        "similar": False,
    }
    req = requests.post(f"{url}/recommend/{bookDataMult[0][0]}", headers=headers, json=data)
    assert req.status_code == _OK
    assert len(req.json()["recommend"]) == 5

def test_no_reviews_book(clear, tokens):
    bookDataMult = getBookDataMult()
    headers1 = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    data = {
        "follows": False,
        "genre": False,
        "similar": False,
    }
    req = requests.post(f"{url}/recommend/{bookDataMult[0][0]}", headers=headers1, json=data)
    assert req.status_code == _OK
    assert len(req.json()["recommend"]) == 5

def test_reviews_for_book(clear, tokens):
    bookDataMult = getBookDataMult()
    headers0 = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/collections", headers=headers0)
    cID = res.json()["collections"][0]["collectionID"]
    requests.post(f"{url}/collections/{cID}/add/{bookDataMult[0][0]}", headers=headers0)
    requests.post(f"{url}/collections/{cID}/add/{bookDataMult[1][0]}", headers=headers0)
    requests.post(f"{url}/collections/{cID}/add/{bookDataMult[2][0]}", headers=headers0)

    payload = {
        "rating": 4,
    }
    requests.post(f"{url}/books/{bookDataMult[0][0]}/review/add", json=payload, headers=headers0)
    payload = {
        "rating": 2,
    }
    requests.post(f"{url}/books/{bookDataMult[1][0]}/review/add", json=payload, headers=headers0)
    payload = {
        "rating": 5,
    }
    requests.post(f"{url}/books/{bookDataMult[2][0]}/review/add", json=payload, headers=headers0)    

    headers1 = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    data = {
        "follows": False,
        "genre": False,
        "similar": False,
    }
    req = requests.post(f"{url}/recommend/{bookDataMult[0][0]}", headers=headers1, json=data)
    assert req.status_code == _OK
    assert len(req.json()["recommend"]) == 5
    assert req.json()["recommend"][0]["bookID"] == bookDataMult[2][0]
    assert req.json()["recommend"][1]["bookID"] == bookDataMult[1][0]

def test_restrict_follows(clear, tokens):
    bookDataMult = getBookDataMult()
    headers0 = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/collections", headers=headers0)
    cID = res.json()["collections"][0]["collectionID"]
    requests.post(f"{url}/collections/{cID}/add/{bookDataMult[0][0]}", headers=headers0)
    requests.post(f"{url}/collections/{cID}/add/{bookDataMult[1][0]}", headers=headers0)
    requests.post(f"{url}/collections/{cID}/add/{bookDataMult[2][0]}", headers=headers0)
    requests.post(f"{url}/collections/{cID}/add/{bookDataMult[4][0]}", headers=headers0)
    requests.post(f"{url}/collections/{cID}/add/{bookDataMult[6][0]}", headers=headers0)
    requests.post(f"{url}/collections/{cID}/add/{bookDataMult[9][0]}", headers=headers0)

    payload = {
        "rating": 4,
    }
    requests.post(f"{url}/books/{bookDataMult[0][0]}/review/add", json=payload, headers=headers0)
    payload = {
        "rating": 2,
    }
    requests.post(f"{url}/books/{bookDataMult[1][0]}/review/add", json=payload, headers=headers0)
    payload = {
        "rating": 3,
    }
    requests.post(f"{url}/books/{bookDataMult[2][0]}/review/add", json=payload, headers=headers0)  
    payload = {
        "rating": 5,
    }
    requests.post(f"{url}/books/{bookDataMult[4][0]}/review/add", json=payload, headers=headers0) 
    payload = {
        "rating": 0,
    }
    requests.post(f"{url}/books/{bookDataMult[6][0]}/review/add", json=payload, headers=headers0) 
    payload = {
        "rating": 1,
    }
    requests.post(f"{url}/books/{bookDataMult[9][0]}/review/add", json=payload, headers=headers0)   

    headers1 = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.get(f"{url}/collections", headers=headers1)
    cID1 = res.json()["collections"][0]["collectionID"]
    payload = {
        "rating": 5,
    }
    for i in range(len(bookDataMult)):
        requests.post(f"{url}/collections/{cID1}/add/{bookDataMult[i][0]}", headers=headers1)
        requests.post(f"{url}/books/{bookDataMult[i][0]}/review/add", json=payload, headers=headers1)

    headers2 = {
        "Authorization": f"Bearer {tokens[2]}"
    }
    requests.post(f"{url}/users/follow/a", headers=headers2)
    data = {
        "follows": True,
        "genre": False,
        "similar": False,
    }
    req = requests.post(f"{url}/recommend/{bookDataMult[0][0]}", headers=headers2, json=data)
    assert req.status_code == _OK
    assert len(req.json()["recommend"]) == 5
    assert req.json()["recommend"][0]["bookID"] == bookDataMult[4][0]
    assert req.json()["recommend"][1]["bookID"] == bookDataMult[2][0]
    assert req.json()["recommend"][2]["bookID"] == bookDataMult[1][0]
    assert req.json()["recommend"][3]["bookID"] == bookDataMult[9][0]
    assert req.json()["recommend"][4]["bookID"] == bookDataMult[6][0]

def test_restrict_genre_no_reviews(clear, tokens):
    bookDataMult = getBookDataMult()
    headers2 = {
        "Authorization": f"Bearer {tokens[2]}"
    }
    data = {
        "follows": False,
        "genre": True,
        "similar": False,
    }
    req = requests.post(f"{url}/recommend/{bookDataMult[0][0]}", headers=headers2, json=data)
    assert req.status_code == _OK
    assert len(req.json()["recommend"]) == 5
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f"""select genre from books
where bookID = "{bookDataMult[0][0]}";""")
    genre = cur.fetchone()[0]
    for b in req.json()["recommend"]:
        cur.execute(f"""select genre from books
where bookID = "{b["bookID"]}";""")
        assert cur.fetchone()[0] == genre
    cur.close()
    conn.close()

def test_restrict_genre_reviews(clear, tokens):
    bookDataMult = getBookDataMult()
    headers0 = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/collections", headers=headers0)
    cID0 = res.json()["collections"][0]["collectionID"]
    payload = {
        "rating": 5,
    }
    for i in range(len(bookDataMult)):
        requests.post(f"{url}/collections/{cID0}/add/{bookDataMult[i][0]}", headers=headers0)
        requests.post(f"{url}/books/{bookDataMult[i][0]}/review/add", json=payload, headers=headers0)   

    headers2 = {
        "Authorization": f"Bearer {tokens[2]}"
    }
    data = {
        "follows": False,
        "genre": True,
        "similar": False,
    }
    req = requests.post(f"{url}/recommend/{bookDataMult[0][0]}", headers=headers2, json=data)
    assert req.status_code == _OK
    assert len(req.json()["recommend"]) == 5
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f"""select genre from books
where bookID = "{bookDataMult[0][0]}";""")
    genre = cur.fetchone()[0]
    for b in req.json()["recommend"]:
        cur.execute(f"""select genre from books
where bookID = "{b["bookID"]}";""")
        assert cur.fetchone()[0] == genre
    cur.close()
    conn.close()

def test_already_read(clear, tokens):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("select * from books order by random() limit 500;")
    bookDataMult = cur.fetchall()
    cur.close()
    conn.close()
    bIDs = [b[0] for b in bookDataMult]

    headers0 = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/collections", headers=headers0)
    cID0 = res.json()["collections"][0]["collectionID"]

    for book in bookDataMult:
        requests.post(f"{url}/collections/{cID0}/add/{book[0]}", headers=headers0)

    data = {
        "follows": False,
        "genre": False,
        "similar": False,
    }
    for _ in range(50):
        req = requests.post(f"{url}/recommend/{bookDataMult[0][0]}", headers=headers0, json=data)
        assert req.status_code == _OK
        reqJson = req.json()["recommend"]
        assert len(reqJson) == 5
        for i in range(5):
            assert reqJson[i]["bookID"] not in bIDs

def test_restrict_similar_none(clear, tokens):
    bookDataMult = getBookDataMult()
    headers0 = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    data = {
        "follows": False,
        "genre": False,
        "similar": True,
    }
    req = requests.post(f"{url}/recommend/{bookDataMult[0][0]}", headers=headers0, json=data)
    assert req.status_code == _OK
    assert len(req.json()["recommend"]) == 5

def test_restrict_similar_exists(clear, tokens):
    bookDataMult = getBookDataMult()
    headers0 = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/collections", headers=headers0)
    cID0 = res.json()["collections"][0]["collectionID"]
    payload = {
        "rating": 5,
    }
    for i in range(4, 10):
        requests.post(f"{url}/collections/{cID0}/add/{bookDataMult[i][0]}", headers=headers0)
        requests.post(f"{url}/books/{bookDataMult[i][0]}/review/add", json=payload, headers=headers0)   

    headers1 = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.get(f"{url}/collections", headers=headers1)
    cID1 = res.json()["collections"][0]["collectionID"]
    payload = {
        "rating": 0,
    }
    for i in range(5):
        requests.post(f"{url}/collections/{cID1}/add/{bookDataMult[i][0]}", headers=headers1)
        requests.post(f"{url}/books/{bookDataMult[i][0]}/review/add", json=payload, headers=headers1)

    headers2 = {
        "Authorization": f"Bearer {tokens[2]}"
    }
    res = requests.get(f"{url}/collections", headers=headers2)
    cID2 = res.json()["collections"][0]["collectionID"]
    payload = {
        "rating": 3,
    }
    requests.post(f"{url}/collections/{cID2}/add/{bookDataMult[4][0]}", headers=headers2)
    requests.post(f"{url}/books/{bookDataMult[4][0]}/review/add", json=payload, headers=headers2)

    data = {
        "follows": False,
        "genre": False,
        "similar": True,
    }
    req = requests.post(f"{url}/recommend/{bookDataMult[4][0]}", headers=headers2, json=data)
    assert req.status_code == _OK
    reqJson = req.json()["recommend"]
    assert len(reqJson) == 5
    bIDs = [b[0] for b in bookDataMult[4:]]
    for i in range(5):
        assert reqJson[i]["bookID"] in bIDs

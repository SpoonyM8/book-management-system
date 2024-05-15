import pytest
import requests
import sqlite3
from ..config import url, db
from ..src.constant import _OK, _InputError, _UnauthorizedError, _AccessError

@pytest.fixture
def clear():
    requests.delete(f"{url}/clear")

@pytest.fixture
def token():
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

@pytest.fixture
def bookID():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""delete from Books where bookID=1 or bookID=2 or bookID=3;""")
    conn.commit()
    cur.execute("""insert into Books (bookId, title, author) values (1, "Harry Potter and the Philosopher's Stone", "J.K. Rowling"),
    (2, "Dune", "Frank Herbert"), (3, "A Game of Thrones", "George R. R. Martin")""")
    conn.commit()
    cur.close()
    conn.close()
    return 1, 2, 3

@pytest.fixture
def review(bookID, token):
    token, collectionID = token
    payload = {
        "rating": 2,
        "comment": "i like this"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    addToCollection(collectionID, bookID[0], headers)
    res = requests.post(f"{url}/books/{bookID[0]}/review/add", json=payload, headers=headers)
    return bookID[0]

def addToCollection(collectionID, bookID, headers):
    requests.post(f"{url}/sharedCollection/{collectionID}/add/{bookID}", headers=headers)

def test_add_review_valid(clear, bookID, token):
    token, collectionID = token
    payload = {
        "rating": 2
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    addToCollection(collectionID, bookID[0], headers)
    res = requests.post(f"{url}/books/{bookID[0]}/review/add", json=payload, headers=headers)
    assert res.status_code == _OK

def test_add_review_invalid_not_read(clear, bookID, token):
    token, collectionID = token
    payload = {
        "rating": 2
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.post(f"{url}/books/{bookID[0]}/review/add", json=payload, headers=headers)
    assert res.status_code == _AccessError

def test_add_review_comment_valid(clear, bookID, token):
    token, collectionID = token
    payload = {
        "rating": 2,
        "comment": "i like this"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    addToCollection(collectionID, bookID[2], headers)
    res = requests.post(f"{url}/books/{bookID[2]}/review/add", json=payload, headers=headers)
    assert res.status_code == _OK

def test_add_review_no_rating(clear, bookID, token):
    token, collectionID = token
    payload = {
        "comment": "i like this"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    addToCollection(collectionID, bookID[2], headers)
    res = requests.post(f"{url}/books/{bookID[2]}/review/add", json=payload, headers=headers)
    assert res.status_code == _InputError

def test_add_review_rating_invalid(clear, bookID, token):
    token, collectionID = token
    payload = {
        "rating": -1,
        "comment": "i like this"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    addToCollection(collectionID, bookID[2], headers)
    res = requests.post(f"{url}/books/{bookID[2]}/review/add", json=payload, headers=headers)
    assert res.status_code == _InputError

    payload = {
        "rating": 6,
        "comment": "i like this"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    addToCollection(collectionID, bookID[2], headers)
    res = requests.post(f"{url}/books/{bookID[2]}/review/add", json=payload, headers=headers)
    assert res.status_code == _InputError

def test_add_review_comment_invalid(clear, bookID, token):
    token, collectionID = token
    comment = "a"*1000+"a"
    payload = {
        "rating": 4,
        "comment": comment
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    addToCollection(collectionID, bookID[1], headers)
    res = requests.post(f"{url}/books/{bookID[1]}/review/add", json=payload, headers=headers)
    assert res.status_code == _InputError

def test_add_review_already(clear, bookID, token):
    token, collectionID = token
    payload = {
        "rating": 4,
        "comment": "nice"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    addToCollection(collectionID, bookID[1], headers)
    res = requests.post(f"{url}/books/{bookID[1]}/review/add", json=payload, headers=headers)
    assert res.status_code == _OK

    payload = {
        "rating": 3,
        "comment": "again"
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }
    addToCollection(collectionID, bookID[1], headers)
    res = requests.post(f"{url}/books/{bookID[1]}/review/add", json=payload, headers=headers)
    assert res.status_code == _AccessError

def test_delete_review_valid(clear, review, token):
    token, collectionID = token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.delete(f"{url}/books/{review}/review/delete", headers=headers)
    assert res.status_code == _OK

def test_delete_review_invalid_none(clear, token):
    token, collectionID = token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.delete(f"{url}/books/{review}/review/delete", headers=headers)
    assert res.status_code == _AccessError

def test_valid_review_multiple(clear, review, token):
    token, collectionID = token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.delete(f"{url}/books/{review}/review/delete", headers=headers)
    assert res.status_code == _OK

    payload = {
        "rating": 3,
        "comment": "again"
    }
    res = requests.post(f"{url}/books/{review}/review/add", json=payload, headers=headers)
    assert res.status_code == _OK

    res = requests.delete(f"{url}/books/{review}/review/delete", headers=headers)
    assert res.status_code == _OK



def test_get_reviews(clear, bookID, tokens):
    headers0 = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/books/{bookID[0]}/review/get", headers=headers0)
    assert res.status_code == _OK

    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers0)
    collectionID0 = res.json()["collectionID"]
    addToCollection(collectionID0, bookID[0], headers0)
    headers1 = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers1)
    collectionID1 = res.json()["collectionID"]
    addToCollection(collectionID1, bookID[0], headers1)
    headers2 = {
        "Authorization": f"Bearer {tokens[2]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers2)
    collectionID2 = res.json()["collectionID"]
    addToCollection(collectionID2, bookID[0], headers2)
    
    payload = {
        "rating": 3,
        "comment": "again"
    }
    res = requests.post(f"{url}/books/{bookID[0]}/review/add", json=payload, headers=headers0)
    assert res.status_code == _OK

    payload = {
        "rating": 1,
    }
    res = requests.post(f"{url}/books/{bookID[0]}/review/add", json=payload, headers=headers1)
    assert res.status_code == _OK

    payload = {
        "rating": 5,
        "comment": "good comment"
    }
    res = requests.post(f"{url}/books/{bookID[0]}/review/add", json=payload, headers=headers2)
    assert res.status_code == _OK

    res = requests.get(f"{url}/books/{bookID[0]}/review/get", headers=headers0)
    assert res.status_code == _OK
    resJson = res.json()
    assert len(resJson["reviews"]) == 3
    assert resJson["reviews"][0]["username"] == "c"
    assert resJson["reviews"][0]["rating"] == 5.0
    assert resJson["reviews"][0]["comment"] == "good comment"
    assert "timeAdded" in list(resJson["reviews"][0].keys())
    assert resJson["reviews"][1]["username"] == "b"
    assert resJson["reviews"][1]["rating"] == 1.0
    assert resJson["reviews"][1]["comment"] == ""
    assert "timeAdded" in list(resJson["reviews"][1].keys())
    assert resJson["reviews"][2]["username"] == "a"
    assert resJson["reviews"][2]["rating"] == 3.0
    assert resJson["reviews"][2]["comment"] == "again"
    assert "timeAdded" in list(resJson["reviews"][2].keys())

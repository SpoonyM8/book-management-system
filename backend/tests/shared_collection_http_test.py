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

def test_create_shared_collection(clear, tokens):
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()
    assert len(resJson) == 1
    assert "collectionID" in resJson.keys()

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/b", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/b", headers=headers)
    assert res.status_code == _OK

def test_delete_shared_collection(clear, tokens):
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/sharedCollection/delete/a", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    assert res.status_code == _OK
    collectionID1 = res.json()["collectionID"]

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/sharedCollection/delete/{collectionID1}", headers=headers)
    assert res.status_code == _AccessError

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    assert res.status_code == _OK
    collectionID2 = res.json()["collectionID"]

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/sharedCollection/delete/{collectionID2}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/sharedCollection/delete/{collectionID1}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/sharedCollection/delete/{collectionID2}", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/sharedCollection/delete/{collectionID1}", headers=headers)
    assert res.status_code == _InputError

def test_join_shared_collection(clear, tokens):
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/join/a", headers=headers)
    assert res.status_code == _InputError
    
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    assert res.status_code == _OK
    collectionID1 = res.json()["collectionID"]

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/join/{collectionID1}", headers=headers)
    assert res.status_code == _AccessError

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/join/{collectionID1}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/join/{collectionID1}", headers=headers)
    assert res.status_code == _AccessError

def test_leave_shared_collection(clear, tokens):
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/sharedCollection/leave/a", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    assert res.status_code == _OK
    collectionID1 = res.json()["collectionID"]

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/sharedCollection/leave/{collectionID1}", headers=headers)
    assert res.status_code == _AccessError
    
    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/sharedCollection/leave/{collectionID1}", headers=headers)
    assert res.status_code == _AccessError

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/join/{collectionID1}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/sharedCollection/leave/{collectionID1}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/sharedCollection/leave/{collectionID1}", headers=headers)
    assert res.status_code == _AccessError

def test_add_book_shared_collection(clear, tokens):
    bookData = getBookData()
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/a/add/{bookData[0]}", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    assert res.status_code == _OK
    collectionID1 = res.json()["collectionID"]

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookData[0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookData[0]}", headers=headers)
    assert res.status_code == _AccessError

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/join/{collectionID1}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookData[0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookData[0]}", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookData[0]}", headers=headers)
    assert res.status_code == _InputError

def test_remove_book_shared_collection(clear, tokens): 
    bookData = getBookData()
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/sharedCollection/a/remove/{bookData[0]}", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    assert res.status_code == _OK
    collectionID1 = res.json()["collectionID"]

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/sharedCollection/{collectionID1}/remove/{bookData[0]}", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookData[0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/sharedCollection/{collectionID1}/remove/{bookData[0]}", headers=headers)
    assert res.status_code == _AccessError

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/join/{collectionID1}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookData[0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/sharedCollection/{collectionID1}/remove/{bookData[0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookData[0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/sharedCollection/{collectionID1}/remove/{bookData[0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/sharedCollection/{collectionID1}/remove/{bookData[0]}", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/sharedCollection/{collectionID1}/remove/{bookData[0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/sharedCollection/{collectionID1}/remove/{bookData[0]}", headers=headers)
    assert res.status_code == _InputError

def compare_details_lists(a, b):
    if len(a) != len(b):
        return False
    for book1 in a:
        for book2 in b:
            bookID = book1["bookID"] == book2["bookID"]
            title = book1["title"] == book2["title"]
            author = book1["author"] == book2["author"]
            numRead = book1["numRead"] == book2["numRead"]
            if bookID and title and author and numRead:
                break
        else:
            return False
    return True

def test_shared_collection_details(clear, tokens):
    bookDataMult = getBookDataMult()

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/sharedCollection/a/details", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    assert res.status_code == _OK
    collectionID1 = res.json()["collectionID"]

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/sharedCollection/{collectionID1}/details", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()
    assert resJson["owner"] == "a"
    assert int(resJson["numBooks"]) == 0
    assert int(resJson["numMembers"]) == 1
    assert resJson["books"] == []
    
    for i in range(1, len(tokens)):
        headers = {
            "Authorization": f"Bearer {tokens[i]}"
        }
        res = requests.post(f"{url}/sharedCollection/join/{collectionID1}", headers=headers)
        assert res.status_code == _OK

    
    headers = {
        "Authorization": f"Bearer {tokens[-1]}"
    }
    res = requests.get(f"{url}/sharedCollection/{collectionID1}/details", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()
    assert resJson["owner"] == "a"
    assert int(resJson["numBooks"]) == 0
    assert int(resJson["numMembers"]) == len(tokens)
    assert resJson["books"] == []


    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[0][0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[0][0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[2]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[0][0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[1][0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[3]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[2][0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[4]}"
    }
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[2][0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/sharedCollection/{collectionID1}/remove/{bookDataMult[0][0]}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[-1]}"
    }
    res = requests.get(f"{url}/sharedCollection/{collectionID1}/details", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()
    assert resJson["owner"] == "a"
    assert int(resJson["numBooks"]) == 3
    assert int(resJson["numMembers"]) == len(tokens)
    print(resJson["books"])
    assert compare_details_lists(resJson["books"], [
        {
            "bookID":  bookDataMult[0][0],
            "title": bookDataMult[0][1],
            "author": bookDataMult[0][2],
            "numRead": 2
        },
        {
            "bookID":  bookDataMult[1][0],
            "title": bookDataMult[1][1],
            "author": bookDataMult[1][2],
            "numRead": 1
        },
        {
            "bookID":  bookDataMult[2][0],
            "title": bookDataMult[2][1],
            "author": bookDataMult[2][2],
            "numRead": 2
        }
    ])

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.delete(f"{url}/sharedCollection/leave/{collectionID1}", headers=headers)
    assert res.status_code == _OK


    headers = {
        "Authorization": f"Bearer {tokens[-1]}"
    }
    res = requests.get(f"{url}/sharedCollection/{collectionID1}/details", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()
    assert resJson["owner"] == "a"
    assert int(resJson["numBooks"]) == 2
    assert int(resJson["numMembers"]) == len(tokens) - 1
    print(resJson["books"])
    assert compare_details_lists(resJson["books"], [
        {
            "bookID":  bookDataMult[0][0],
            "title": bookDataMult[0][1],
            "author": bookDataMult[0][2],
            "numRead": 2
        },
        {
            "bookID":  bookDataMult[2][0],
            "title": bookDataMult[2][1],
            "author": bookDataMult[2][2],
            "numRead": 2
        }
    ])

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/sharedCollection/delete/{collectionID1}", headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/sharedCollection/{collectionID1}/details", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[-1]}"
    }
    res = requests.get(f"{url}/sharedCollection/{collectionID1}/details", headers=headers)
    assert res.status_code == _InputError


def test_shared_collection_user(clear, tokens):
    bookDataMult = getBookDataMult()

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    assert res.status_code == _OK
    collectionID1 = res.json()["collectionID"]

    for i in range(1, len(tokens)):
        headers0 = {
            "Authorization": f"Bearer {tokens[i]}"
        }
        res = requests.post(f"{url}/sharedCollection/join/{collectionID1}", headers=headers0)
        assert res.status_code == _OK

    requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[0][0]}", headers=headers)
    requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[1][0]}", headers=headers)
    requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[2][0]}", headers=headers)

    headers1 = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[2][0]}", headers=headers1)
    requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[3][0]}", headers=headers1)

    headers2 = {
        "Authorization": f"Bearer {tokens[2]}"
    }
    requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[1][0]}", headers=headers2)
    requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[2][0]}", headers=headers2)
    requests.post(f"{url}/sharedCollection/{collectionID1}/add/{bookDataMult[4][0]}", headers=headers2)

    res = requests.get(f"{url}/sharedCollection", headers=headers)
    assert res.status_code == _OK
    collections = res.json()["collections"]
    assert len(collections) == 1
    assert len(collections[0]["books"]) == 5
    assert collections[0]["books"][0][0] == bookDataMult[4][0]
    assert collections[0]["books"][1][0] == bookDataMult[3][0]
    assert collections[0]["books"][2][0] == bookDataMult[2][0]
    assert collections[0]["books"][3][0] == bookDataMult[1][0]
    assert collections[0]["books"][4][0] == bookDataMult[0][0]
    assert collections[0]["isOwner"]
    assert collections[0]["collectionName"] == "a"
    assert collections[0]["collectionID"] == collectionID1

    res = requests.get(f"{url}/sharedCollection", headers=headers1)
    assert res.status_code == _OK
    collections = res.json()["collections"]
    assert len(collections) == 1
    assert len(collections[0]["books"]) == 5
    assert collections[0]["books"][0][0] == bookDataMult[4][0]
    assert collections[0]["books"][1][0] == bookDataMult[3][0]
    assert collections[0]["books"][2][0] == bookDataMult[2][0]
    assert collections[0]["books"][3][0] == bookDataMult[1][0]
    assert collections[0]["books"][4][0] == bookDataMult[0][0]
    assert not collections[0]["isOwner"]
    assert collections[0]["collectionName"] == "a"
    assert collections[0]["collectionID"] == collectionID1

    res = requests.get(f"{url}/sharedCollection/user/b", headers=headers1)
    assert res.status_code == _OK
    collections = res.json()["collections"]
    assert len(collections) == 1
    assert len(collections[0]["books"]) == 5
    assert collections[0]["books"][0][0] == bookDataMult[4][0]
    assert collections[0]["books"][1][0] == bookDataMult[3][0]
    assert collections[0]["books"][2][0] == bookDataMult[2][0]
    assert collections[0]["books"][3][0] == bookDataMult[1][0]
    assert collections[0]["books"][4][0] == bookDataMult[0][0]
    assert not collections[0]["isOwner"]
    assert collections[0]["collectionName"] == "a"
    assert collections[0]["collectionID"] == collectionID1

def test_is_member(clear, tokens):
    headers1 = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.get(f"{url}/sharedCollection/none/is_member/b", headers=headers1)
    assert res.status_code == _OK
    assert res.json()["is_member"] == False

    headers0 = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers0)
    collectionID = res.json()["collectionID"]
    res = requests.get(f"{url}/sharedCollection/{collectionID}/is_member/a", headers=headers0)
    assert res.status_code == _OK
    assert res.json()["is_member"] == True

    res = requests.get(f"{url}/sharedCollection/{collectionID}/is_member/b", headers=headers1)
    assert res.status_code == _OK
    assert res.json()["is_member"] == False

    requests.post(f"{url}/sharedCollection/join/{collectionID}", headers=headers1)
    res = requests.get(f"{url}/sharedCollection/{collectionID}/is_member/b", headers=headers1)
    assert res.status_code == _OK
    assert res.json()["is_member"] == True

def test_shared_collections_all(clear, tokens):
    headers1 = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.get(f"{url}/sharedCollection/all", headers=headers1)
    assert res.status_code == _OK
    assert res.json()["collections"] == []

    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers1)
    cID0 = res.json()["collectionID"]
    res = requests.get(f"{url}/sharedCollection/all", headers=headers1)
    cIDs = [c["collectionID"] for c in res.json()["collections"]]
    assert len(cIDs) == 1
    assert cID0 in cIDs

    res = requests.post(f"{url}/sharedCollection/create/b", headers=headers1)
    cID1 = res.json()["collectionID"]
    res = requests.get(f"{url}/sharedCollection/all", headers=headers1)
    cIDs = [c["collectionID"] for c in res.json()["collections"]]
    assert len(cIDs) == 2
    assert cID0 in cIDs
    assert cID1 in cIDs

    res = requests.post(f"{url}/sharedCollection/create/c", headers=headers1)
    cID2 = res.json()["collectionID"]
    res = requests.get(f"{url}/sharedCollection/all", headers=headers1)
    cIDs = [c["collectionID"] for c in res.json()["collections"]]
    assert len(cIDs) == 3
    assert cID0 in cIDs
    assert cID1 in cIDs
    assert cID2 in cIDs

    res = requests.delete(f"{url}/sharedCollection/delete/{cID1}", headers=headers1)
    res = requests.get(f"{url}/sharedCollection/all", headers=headers1)
    cIDs = [c["collectionID"] for c in res.json()["collections"]]
    assert len(cIDs) == 2
    assert cID0 in cIDs
    assert cID2 in cIDs

    headers0 = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    bookDataMult = getBookDataMult()
    requests.delete(f"{url}/sharedCollection/delete/{cID2}", headers=headers1)
    requests.post(f"{url}/sharedCollection/{cID0}/add/{bookDataMult[0][0]}", headers=headers1)
    requests.post(f"{url}/sharedCollection/{cID0}/add/{bookDataMult[1][0]}", headers=headers1)
    requests.post(f"{url}/sharedCollection/join/{cID0}", headers=headers0)
    res = requests.get(f"{url}/sharedCollection/all", headers=headers1)
    cIDs = [c["collectionID"] for c in res.json()["collections"]]
    assert len(cIDs) == 1
    assert cID0 in cIDs
    assert len(res.json()["collections"][0]["books"]) == 2
    b0 = [bookDataMult[0][0], bookDataMult[0][1], bookDataMult[0][5], bookDataMult[0][2]]
    b1 = [bookDataMult[1][0], bookDataMult[1][1], bookDataMult[1][5], bookDataMult[1][2]]
    assert b0 in res.json()["collections"][0]["books"]
    assert b1 in res.json()["collections"][0]["books"]



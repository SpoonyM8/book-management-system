import pytest
import requests
import sqlite3
from datetime import datetime
from json import loads
from ..config import url, db
from ..src.constant import _OK, _InputError, _AccessError

@pytest.fixture
def clear():
    requests.delete(f"{url}/clear")

@pytest.fixture
def tokens():
    users = ["a", "b"]
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

### tests

def test_create_goal(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet = {
        "target": 5,
        "month": 5,
        "year": 2023
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)
    assert res.status_code == _OK

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)
    assert res.status_code == _OK

def test_wrong_target_goal(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet1 = {
        "target": 0,
        "month": 5,
        "year": 2023
    } 
    packet2 = {
        "target": -5,
        "month": 5,
        "year": 2023
    }  

    res = requests.post(f"{url}/goals/create", json=packet1, headers=headers)
    assert res.status_code == _InputError

    res = requests.post(f"{url}/goals/create", json=packet2, headers=headers)
    assert res.status_code == _InputError 

def test_wrong_date_goal(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet1 = {
        "target": 5,
        "month": 3,
        "year": 2023
    } 
    packet2 = {
        "target": 5,
        "month": 3,
        "year": 2022
    }  
    packet3 = {
        "target": 5,
        "month": 5,
        "year": 2022
    } 

    res = requests.post(f"{url}/goals/create", json=packet1, headers=headers)
    assert res.status_code == _InputError 

    res = requests.post(f"{url}/goals/create", json=packet2, headers=headers)
    assert res.status_code == _InputError  

    res = requests.post(f"{url}/goals/create", json=packet3, headers=headers)
    assert res.status_code == _InputError  


def test_user_goals(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/goals", headers=headers)
    assert res.status_code == _OK
    assert 'goals' in res.json().keys() and len(res.json()) == 1
    assert len(res.json()['goals']) == 0

    packet = {
        "target": 5,
        "month": 5,
        "year": 2023
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)
    assert res.status_code == _OK

    res = requests.get(f"{url}/goals", headers=headers)
    assert res.status_code == _OK
    assert len(res.json()['goals']) == 1

def test_user_goal_details(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet = {
        "target": 5,
        "month": 5,
        "year": 2023
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)
    assert res.status_code == _OK
    goalID = res.json()['goalID']

    res = requests.get(f"{url}/goals", headers=headers)
    assert res.status_code == _OK
    goals = res.json()['goals']
    assert len(goals) == 1

    goalDict = goals[0]
    assert goalDict['goalID'] == goalID
    assert goalDict['username'] == 'a'
    assert goalDict['numRead'] == 0
    assert goalDict['numTarget'] == packet['target']
    assert goalDict['numMonth'] == packet['month']
    assert goalDict['numYear'] == packet['year']
    assert goalDict['isCompleted'] == False

def test_goal_update(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet = {
        "target": 5,
        "month": 5,
        "year": 2023
    }  
    updatePacket = {
        "target": 6
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)
    goalID = res.json()["goalID"]
    print(goalID)

    res = requests.get(f"{url}/goals", headers=headers)
    goals = res.json()['goals']
    assert len(goals) == 1
    goalDict = goals[0]
    assert goalDict['numTarget'] == packet['target']

    res = requests.post(f"{url}/goals/update/{goalID}", json=updatePacket, headers=headers)
    assert res.status_code == _OK

    res = requests.get(f"{url}/goals", headers=headers)
    goals = res.json()['goals']
    assert len(goals) == 1
    goalDict = goals[0]
    assert goalDict['numTarget'] == updatePacket['target']

    res = requests.post(f"{url}/goals/update/wrongID", json=updatePacket, headers=headers)
    assert res.status_code == _InputError

def test_current_month_goal_update(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet = {
        "target": 5,
        "month": datetime.now().month,
        "year": datetime.now().year
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)
    assert res.status_code == _OK
    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 0

    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    collection = res.json()["collections"][0]
    collectionID = collection["collectionID"]
    books = getBookDataMult()

    requests.post(f"{url}/collections/{collectionID}/add/{books[0][0]}", headers=headers)
    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 1
    assert goalDict['isCompleted'] == (goalDict['numRead'] >= goalDict['numTarget'])
    assert goalDict['isCompleted'] == False

    requests.post(f"{url}/collections/{collectionID}/add/{books[1][0]}", headers=headers)
    res = requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 2
    assert goalDict['isCompleted'] == (goalDict['numRead'] >= goalDict['numTarget'])
    assert goalDict['isCompleted'] == False

def test_remove_goal(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet = {
        "target": 5,
        "month": 5,
        "year": 2023
    }

    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)
    goalID = res.json()["goalID"]

    res = requests.get(f"{url}/goals", headers=headers)
    assert res.status_code == _OK
    goals = res.json()['goals']
    assert len(goals) == 1  


    res = requests.delete(f"{url}/goals/remove/{goalID}", headers=headers)
    assert res.status_code == _OK

    res = requests.get(f"{url}/goals", headers=headers)
    assert res.status_code == _OK
    goals = res.json()['goals']
    assert len(goals) == 0  

    res = requests.delete(f"{url}/goals/remove/{goalID}", headers=headers)
    assert res.status_code == _InputError

def test_current_goal_complete(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet = {
        "target": 3,
        "month": datetime.now().month,
        "year": datetime.now().year
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)

    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    collection = res.json()["collections"][0]
    collectionID = collection["collectionID"]
    books = getBookDataMult()

    requests.post(f"{url}/collections/{collectionID}/add/{books[0][0]}", headers=headers)
    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 1
    assert goalDict['isCompleted'] == (goalDict['numRead'] >= goalDict['numTarget'])
    assert goalDict['isCompleted'] == False


    requests.post(f"{url}/collections/{collectionID}/add/{books[1][0]}", headers=headers)
    res = requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 2
    assert goalDict['isCompleted'] == (goalDict['numRead'] >= goalDict['numTarget'])
    assert goalDict['isCompleted'] == False


    requests.post(f"{url}/collections/{collectionID}/add/{books[2][0]}", headers=headers)
    res = requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 3
    assert goalDict['isCompleted'] == (goalDict['numRead'] >= goalDict['numTarget'])
    assert goalDict['isCompleted'] == True

def test_correct_month_update(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet = { # next month
        "target": 3,
        "month": datetime.now().month + 1,
        "year": datetime.now().year
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)

    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    collection = res.json()["collections"][0]
    collectionID = collection["collectionID"]
    book = getBookData()

    requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=headers)
    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 0


def test_removed_book_not_counted(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet = {
        "target": 3,
        "month": datetime.now().month,
        "year": datetime.now().year
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)

    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    collection = res.json()["collections"][0]
    collectionID = collection["collectionID"]
    book = getBookData()

    requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=headers)
    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 1
    
    res = requests.delete(f"{url}/collections/{collectionID}/remove/{book[0]}", headers=headers)
    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 1

    requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=headers)
    assert res.status_code == _OK # adding book back after removing it
    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 1

def test_book_added_second_collection(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    requests.post(f"{url}/collections/create/a", headers=headers)

    packet = { 
        "target": 3,
        "month": datetime.now().month,
        "year": datetime.now().year
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)

    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    collections = res.json()["collections"]
    collectionID1 = collections[0]["collectionID"]
    collectionID2 = collections[1]["collectionID"]

    book = getBookData()

    requests.post(f"{url}/collections/{collectionID1}/add/{book[0]}", headers=headers)
    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 1

    requests.post(f"{url}/collections/{collectionID2}/add/{book[0]}", headers=headers)
    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 1

def test_user_goal_independant(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet = { 
        "target": 3,
        "month": datetime.now().month,
        "year": datetime.now().year
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)
    assert res.status_code == _OK
    res = requests.get(f"{url}/collections/user/{usernames[1]}", headers=headers)
    collection = res.json()["collections"][0]
    collectionID = collection["collectionID"]
    book = getBookData()
    requests.post(f"{url}/collections/{collectionID}/add/{book[0]}", headers=headers)
    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 1

    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }

    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 0


def test_shared_goals(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet = {
        "target": 3,
        "month": datetime.now().month,
        "year": datetime.now().year
    }
    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)

    res = requests.post(f"{url}/sharedCollection/create/a", headers=headers)
    assert res.status_code == _OK
    collectionID1 = res.json()["collectionID"]

    book = getBookData()
    res = requests.post(f"{url}/sharedCollection/{collectionID1}/add/{book[0]}", headers=headers)
    assert res.status_code == _OK

    res =requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 1
    assert goalDict['isCompleted'] == (goalDict['numRead'] >= goalDict['numTarget'])
    assert goalDict['isCompleted'] == False


def test_book_read_before_current_goal(clear, tokens):
    tokens, usernames = tokens
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    packet = {
        "target": 5,
        "month": datetime.now().month,
        "year": datetime.now().year
    }


    res = requests.get(f"{url}/collections/user/{usernames[0]}", headers=headers)
    collection = res.json()["collections"][0]
    collectionID = collection["collectionID"]
    books = getBookDataMult()

    requests.post(f"{url}/collections/{collectionID}/add/{books[0][0]}", headers=headers)

    requests.post(f"{url}/collections/{collectionID}/add/{books[1][0]}", headers=headers)

    res = requests.post(f"{url}/goals/create", json=packet, headers=headers)
    assert res.status_code == _OK
    res = requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 2

    requests.post(f"{url}/collections/{collectionID}/add/{books[2][0]}", headers=headers)
    res = requests.get(f"{url}/goals", headers=headers)
    goalDict = res.json()['goals'][0]
    assert goalDict['numRead'] == 3










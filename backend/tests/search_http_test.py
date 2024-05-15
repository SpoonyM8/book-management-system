import pytest
import requests
import sqlite3
from json import dumps
from ..config import url, db
from ..src.constant import _OK, _InputError, _UnauthorizedError
from ..database.reset_books import reset_books

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
  return res.json()["token"]

@pytest.fixture
def cur():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""delete from Books;""")
    cur.execute("""insert into Books (bookId, title, author) values (1, "Harry Potter and the Philosopher's Stone", "J.K. Rowling"),
    (2, "Dune", "Frank Herbert"), (3, "A Game of Thrones", "George R. R. Martin"), (4, "A Game of nonsense", "Test Martin"), (5, "Harry Potter and the legacy of Hogwarts", "She who shall not be named");""")
    conn.commit()
    cur.close()
    conn.close()

@pytest.fixture
def curUser():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""insert into Users values ("spoony", "reece", "withers", "reece.withers@email.com", "password123@"), ("BenCrab77", "benjamin", "crab", "bencrab77@email.com", "bencrab77!"), ("beforespoonyafter", "spoony", "spoony", "spoony@email.com", "spoony456$")""")
    conn.commit()
    cur.close()
    conn.close()  

@pytest.fixture
def reset_db():
  reset_books()

def test_single_result_title_only(clear, token, cur):
  payload = {
    "title": "Dune"
  }
  headers = {
    "Authorization": f"Bearer {token}"
  }
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _OK
  assert len(res.json()) == 1

def test_single_result_author_only(clear, token, cur):
  payload = {
    "author": "Rowling"
  }
  headers = {
    "Authorization": f"Bearer {token}"
  }
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _OK
  assert len(res.json()) == 1

def test_single_result_title_and_author(clear, token, cur):
  payload = {
    "title": "Game",
    "author": "George R."
  }
  headers = {
    "Authorization": f"Bearer {token}"
  }
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _OK
  assert len(res.json()) == 1

def test_no_matches(clear, token, cur):
  payload = {
    "title": "NoMatches"
  }
  headers = {
    "Authorization": f"Bearer {token}"
  }
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _InputError

def test_multiple_matches_title_only(clear, token, cur):
  payload = {
    "title": "A Game"
  }
  headers = {
    "Authorization": f"Bearer {token}"
  }
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _OK
  assert len(res.json()) == 2

def test_multiple_matches_author_only(clear, token, cur):
  payload = {
    "author": "Martin"
  }
  headers = {
    "Authorization": f"Bearer {token}"
  }
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _OK
  assert len(res.json()) == 2

def test_multiple_matches_author_and_title(clear, token, cur):
  payload = {
    "title": "Harry Potter",
    "author": "J.K"
  }
  headers = {
    "Authorization": f"Bearer {token}"
  }
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _OK
  assert len(res.json()) == 1

def test_single_match_username(clear, token, curUser):
  payload = {
    "username": "crab"
  }
  headers = {
    "Authorization": f"Bearer {token}"
  }  
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _OK
  assert len(res.json()) == 1

def test_multiple_match_username(clear, token, curUser):
  payload = {
    "username": "spoony"
  }
  headers = {
    "Authorization": f"Bearer {token}"
  }  
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _OK
  assert len(res.json()) == 2

def test_no_match_username(clear, token, curUser):
  payload = {
    "username": "idontexist"
  }
  headers = {
    "Authorization": f"Bearer {token}"
  }
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _InputError

# The following tests are not search_http specific, but will be tested here only
def test_expire_jwt(clear, cur, token):
  # custom JWT encoded with expiry set to year 2022
  JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NzMwMzgwNiwianRpIjoiNTk1N2ViYWYtODY1MS00ZjFmLTkzMDQtY2NhNDAzZWIwZDU5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImEiLCJuYmYiOjE2NzczMDM4MDYsImV4cCI6MTY3NTMwNzQwNn0.Wtvp4HCzy4LKsJed06qOCROA1Rye12gmJpC8E2XIDKw"
  payload = {
    "title": "Harry Potter"
  }
  headers = { 
    "Authorization": f"Bearer {JWT}"
  }
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _UnauthorizedError

def test_no_user_jwt(clear, cur, token):
  JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NzMwMzgwNiwianRpIjoiNTk1N2ViYWYtODY1MS00ZjFmLTkzMDQtY2NhNDAzZWIwZDU5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImIiLCJuYmYiOjE2NzczMDM4MDYsImV4cCI6MTY5OTkzMDc0MDZ9.fbs-x7mchwH94xAq2TXxBPTn2dYk7Owmtr5xSkT07w4"
  payload = {
    "title": "Harry Potter"
  }
  headers = { 
    "Authorization": f"Bearer {JWT}"
  }
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _UnauthorizedError

def test_non_jwt(clear, cur, token):
  payload = {
    "title": "Harry Potter"
  }
  headers = { 
    "Authorization": f"234567"
  }
  res = requests.post(f"{url}/search", json=payload, headers=headers)
  assert res.status_code == _UnauthorizedError

def test_missing_header(clear, cur, reset_db):
  payload = {
    "title": "Harry Potter"
  }
  res = requests.post(f"{url}/search", json=payload)
  assert res.status_code == _UnauthorizedError

def test_invalid_bookID(clear, token, curUser):
    bookID = "none"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(f"{url}/books/{bookID}", headers=headers)
    assert res.status_code == _InputError
    

def test_valid_bookID(clear, token, curUser):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("select * from books order by random() limit 1;")
    bookData = cur.fetchone()
    cur.close()
    conn.close()

    headers = {
        "Authorization": f"Bearer {token}"
    }
    res = requests.get(f"{url}/books/{bookData[0]}", headers=headers)
    assert res.status_code == _OK
    assert len(res.json()) >= 9
    resJson = res.json()
    assert resJson["bookID"] == bookData[0]
    assert resJson["title"] == bookData[1]
    assert resJson["author"] == bookData[2]
    assert resJson["yearPublished"] == bookData[3]
    assert resJson["publisher"] == bookData[4]
    assert resJson["coverImage"] == bookData[5]
    assert resJson["numRead"] == bookData[6]
    assert resJson["averageRating"] == bookData[7]
    assert resJson["numRatings"] == bookData[8]

def test_valid_bookID_reviews():
    pass
import pytest
import requests
import sqlite3

from ..config import url, db
from ..src.constant import _OK, _InputError, _AccessError

@pytest.fixture
def clear():
    requests.delete(f"{url}/clear")

@pytest.fixture
def cur():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    return cur

def test_valid_register(clear, cur):
    data = {
        "username": "a",
        "firstName": "b",
        "lastName": "c",
        "email": "b@c.com",
        "password": "aaaaaa1!"
    }
    resp = requests.post(f"{url}/register", json=data)
    assert resp.status_code == _OK
    resp_json = resp.json()
    assert len(resp_json.keys()) == 1
    assert "token" in resp_json

    cur.execute("""select count(*) from Users;""")
    assert cur.fetchone()[0] == 1

    cur.execute("""select count(*) from Collections;""")
    assert cur.fetchone()[0] == 1

def test_valid_register_multiple(clear, cur):
    data1 = {
        "username": "a",
        "firstName": "b",
        "lastName": "c",
        "email": "b@c.com",
        "password": "aaaaaa1!"
    }

    data2 = {
        "username": "b",
        "firstName": "c",
        "lastName": "d",
        "email": "c@d.com",
        "password": "bbbbbb1!"
    }
    
    resp1 = requests.post(f"{url}/register", json=data1)
    assert resp1.status_code == _OK
    resp_json1 = resp1.json()
    assert len(resp_json1.keys()) == 1
    assert "token" in resp_json1

    resp2 = requests.post(f"{url}/register", json=data2)
    assert resp2.status_code == _OK
    resp_json2 = resp2.json()
    assert len(resp_json2.keys()) == 1
    assert "token" in resp_json2

    cur.execute("""select count(*) from Users;""")
    assert cur.fetchone()[0] == 2

def test_invalid_password(clear, cur):
    data = {
        "username": "a",
        "firstName": "b",
        "lastName": "c",
        "email": "b@c.com",
        "password": "aaaaa1!"
    }
    resp = requests.post(f"{url}/register", json=data)
    assert resp.status_code == _InputError

    cur.execute("""select count(*) from Users;""")
    assert cur.fetchone()[0] == 0

def test_invalid_register_username(clear, cur):
    data1 = {
        "username": "a",
        "firstName": "b",
        "lastName": "c",
        "email": "b@c.com",
        "password": "aaaaaa1!"
    }
    resp = requests.post(f"{url}/register", json=data1)
    assert resp.status_code == _OK

    data2 = {
        "username": "a",
        "firstName": "b",
        "lastName": "d",
        "email": "b@d.com",
        "password": "aaaaaa1!"
    }
    resp = requests.post(f"{url}/register", json=data2)
    assert resp.status_code == _InputError

    cur.execute("""select count(*) from Users;""")
    assert cur.fetchone()[0] == 1

def test_invalid_register_email(clear, cur):
    data = {
        "username": "a",
        "firstName": "b",
        "lastName": "c",
        "email": "b@c.c",
        "password": "aaaaaa1!"
    }
    resp = requests.post(f"{url}/register", json=data)
    assert resp.status_code == _InputError

    cur.execute("""select count(*) from Users;""")
    assert cur.fetchone()[0] == 0

def test_invalid_register_email_exists(clear, cur):
    data1 = {
        "username": "a",
        "firstName": "b",
        "lastName": "c",
        "email": "b@c.com",
        "password": "aaaaaa1!"
    }
    resp = requests.post(f"{url}/register", json=data1)
    assert resp.status_code == _OK

    data2 = {
        "username": "b",
        "firstName": "b",
        "lastName": "d",
        "email": "b@c.com",
        "password": "aaaaaa1!"
    }
    resp = requests.post(f"{url}/register", json=data2)
    assert resp.status_code == _InputError

    cur.execute("""select count(*) from Users;""")
    assert cur.fetchone()[0] == 1

def test_missing_field(clear, cur):
    data = {
        "firstName": "b",
        "lastName": "c",
        "email": "b@c.c",
        "password": "aaaaaa1!"
    }
    resp = requests.post(f"{url}/register", json=data)
    assert resp.status_code == _InputError

    data = {
        "username": "a",
        "lastName": "c",
        "email": "b@c.c",
        "password": "aaaaaa1!"
    }
    resp = requests.post(f"{url}/register", json=data)
    assert resp.status_code == _InputError

    data = {
        "username": "a",
        "firstName": "b",
        "email": "b@c.c",
        "password": "aaaaaa1!"
    }
    resp = requests.post(f"{url}/register", json=data)
    assert resp.status_code == _InputError

    data = {
        "username": "a",
        "firstName": "b",
        "lastName": "c",
        "password": "aaaaaa1!"
    }
    resp = requests.post(f"{url}/register", json=data)
    assert resp.status_code == _InputError

    data = {
        "username": "a",
        "firstName": "b",
        "lastName": "c",
        "email": "b@c.c",
    }
    resp = requests.post(f"{url}/register", json=data)
    assert resp.status_code == _InputError

    cur.execute("""select count(*) from Users;""")
    assert cur.fetchone()[0] == 0
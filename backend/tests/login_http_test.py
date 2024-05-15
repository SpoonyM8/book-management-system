import pytest
import requests
import sqlite3

from ..config import url, db
from ..src.constant import _OK, _InputError

@pytest.fixture
def clear():
    requests.delete(f"{url}/clear")

@pytest.fixture
def cur():
    conn = sqlite3.connect(db)
    return conn.cursor()

@pytest.fixture
def register():
    data = {
        "username": "a",
        "firstName": "b",
        "lastName": "c",
        "email": "b@c.com",
        "password": "aaaaaa1!"
    }
    requests.post(f"{url}/register", json=data)

def test_valid_login(clear, cur, register):
    data1 = {
        "username": "a",
        "password": "aaaaaa1!"
    }

    resp1 = requests.post(f"{url}/login", json= data1)
    assert resp1.status_code == _OK
    resp1_json = resp1.json()
    assert len(resp1_json.keys()) == 1
    assert "token" in resp1_json

    data2 = {
        "email": "b@c.com",
        "password": "aaaaaa1!"
    }

    resp2 = requests.post(f"{url}/login", json= data2)
    assert resp2.status_code == _OK 
    resp2_json = resp2.json()
    assert len(resp2_json.keys()) == 1
    assert "token" in resp2_json

def test_invalid_username_login(clear, cur, register):
    data = {
        "username": "b",
        "password": "aaaaaa1!"
    }

    resp = requests.post(f"{url}/login", json= data)
    assert resp.status_code == _InputError

def test_invalid_email_login(clear, cur, register):
    data = {
        "email": "a@b.com",
        "password": "aaaaaa1!"
    }

    resp = requests.post(f"{url}/login", json= data)
    assert resp.status_code == _InputError

def test_incorrect_password_login(clear, cur, register):
    data = {
        "email": "b@c.com",
        "password": "aaaaaa2!"
    }

    resp = requests.post(f"{url}/login", json= data)
    assert resp.status_code == _InputError
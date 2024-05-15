import pytest
import requests
from ..config import url
from ..src.constant import _OK, _InputError, _AccessError

@pytest.fixture
def clear():
    requests.delete(f"{url}/clear")

@pytest.fixture
def register():
    tokens = []
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
    return tokens, users

def test_follow(clear, register):
    tokens, usernames = register
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/users/unfollow/none", headers=headers)
    assert res.status_code == _InputError

    res = requests.post(f"{url}/users/follow/{usernames[0]}", headers=headers)
    assert res.status_code == _InputError

    res = requests.post(f"{url}/users/follow/{usernames[2]}", headers=headers)
    assert res.status_code == _OK

    res = requests.post(f"{url}/users/follow/{usernames[2]}", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[1]}"
    }
    res = requests.post(f"{url}/users/follow/{usernames[2]}", headers=headers)
    assert res.status_code == _OK

    res = requests.post(f"{url}/users/follow/{usernames[2]}", headers=headers)
    assert res.status_code == _InputError

    headers = {
        "Authorization": f"Bearer {tokens[2]}"
    }
    res = requests.post(f"{url}/users/follow/{usernames[0]}", headers=headers)
    assert res.status_code == _OK

    res = requests.post(f"{url}/users/follow/{usernames[0]}", headers=headers)
    assert res.status_code == _InputError

    res = requests.post(f"{url}/users/follow/{usernames[1]}", headers=headers)
    assert res.status_code == _OK

    res = requests.post(f"{url}/users/follow/{usernames[1]}", headers=headers)
    assert res.status_code == _InputError

def test_unfollow(clear, register):
    tokens, usernames = register
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.delete(f"{url}/users/unfollow/none", headers=headers)
    assert res.status_code == _InputError

    res = requests.delete(f"{url}/users/unfollow/{usernames[2]}", headers=headers)
    assert res.status_code == _AccessError

    res = requests.post(f"{url}/users/follow/{usernames[2]}", headers=headers)
    assert res.status_code == _OK

    res = requests.delete(f"{url}/users/unfollow/{usernames[2]}", headers=headers)
    assert res.status_code == _OK

    res = requests.delete(f"{url}/users/unfollow/{usernames[2]}", headers=headers)
    assert res.status_code == _AccessError

def test_followers(clear, register):
    tokens, usernames = register
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/users/followers/none", headers=headers)
    assert res.status_code == _InputError

    res = requests.get(f"{url}/users/followers/{usernames[2]}", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()
    assert len(resJson["followers"]) == 0

    for i in range(9):
        headers = {
            "Authorization": f"Bearer {tokens[i]}"
        }
        res = requests.post(f"{url}/users/follow/{usernames[9]}", headers=headers)
        assert res.status_code == _OK
    
    res = requests.get(f"{url}/users/followers/{usernames[9]}", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()
    assert len(resJson["followers"]) == 9
    for i in range(9):
        assert usernames[i] in resJson["followers"]

    unfollow = [2, 3, 5]
    for i in unfollow:
        headers = {
            "Authorization": f"Bearer {tokens[i]}"
        }
        res = requests.delete(f"{url}/users/unfollow/{usernames[9]}", headers=headers)
        assert res.status_code == _OK

    res = requests.get(f"{url}/users/followers/{usernames[9]}", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()
    assert len(resJson["followers"]) == 6
    for i in range(9):
        if i in unfollow:
            assert usernames[i] not in resJson["followers"]
        else:
            assert usernames[i] in resJson["followers"]

def test_get_following(clear, register):
    tokens, usernames = register
    headers = {
        "Authorization": f"Bearer {tokens[0]}"
    }
    res = requests.get(f"{url}/users/following/none", headers=headers)
    assert res.status_code == _InputError

    res = requests.get(f"{url}/users/following/{usernames[0]}", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()
    assert len(resJson["following"]) == 0    

    for i in range(1,5):
        res = requests.post(f"{url}/users/follow/{usernames[i]}", headers=headers)

    res = requests.get(f"{url}/users/following/{usernames[0]}", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()
    assert len(resJson["following"]) == 4
    for i in range(1,5):
        assert usernames[i] in resJson["following"]

    requests.delete(f"{url}/users/unfollow/{usernames[4]}", headers=headers)
    res = requests.get(f"{url}/users/following/{usernames[0]}", headers=headers)
    assert res.status_code == _OK
    resJson = res.json()
    assert len(resJson["following"]) == 3
    for i in range(1,5):
        if i == 4:
            continue
        assert usernames[i] in resJson["following"] 

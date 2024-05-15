import requests
import sqlite3
from ..config import url, db

# MARCUS #######################################################################

requests.delete(f"{url}/clear")

numbooks = 20

def getBookData():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(f"select * from books order by random() limit {numbooks};")
    bookData = cur.fetchall()
    cur.close()
    conn.close()
    return bookData

books = getBookData() 

data = {
        "username": "lauren92",
        "firstName": "Lauren",
        "lastName": "Taylor",
        "email": "l@t.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
payload = {
        "title": "harry"
    }
res = requests.post(f"{url}/search", json=payload, headers=headers)
harry = res.json()[1]["bookId"]
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[0][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[1][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[2][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[3][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[4][0]}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{books[0][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[1][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[2][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 4,
    }
res = requests.post(f"{url}/books/{books[3][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[4][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[10][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[11][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[12][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[13][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[14][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[10][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[11][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[12][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 2,
    }
res = requests.post(f"{url}/books/{books[13][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{books[14][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "will3m",
        "firstName": "Toby",
        "lastName": "Williams",
        "email": "t@w.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[0][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[1][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[3][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[5][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[6][0]}", headers=headers)
payload = {
        "rating": 4,
    }
res = requests.post(f"{url}/books/{books[0][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 4,
    }
res = requests.post(f"{url}/books/{books[1][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[3][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 4,
    }
res = requests.post(f"{url}/books/{books[5][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 4,
    }
res = requests.post(f"{url}/books/{books[6][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "aBrowne",
        "firstName": "Ash",
        "lastName": "Browne",
        "email": "a@b.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[0][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[1][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[3][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[5][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[6][0]}", headers=headers)
payload = {
        "rating": 0,
    }
res = requests.post(f"{url}/books/{books[0][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 1,
    }
res = requests.post(f"{url}/books/{books[1][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[3][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[5][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[6][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[10][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[11][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[12][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[13][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[14][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[10][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[11][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[12][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[13][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[14][0]}/review/add", headers=headers, json=payload)


data = {
        "username": "goldie95",
        "firstName": "Terry",
        "lastName": "Goldsmith",
        "email": "t@g.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[2][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[3][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[5][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[6][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[2][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[3][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 4,
    }
res = requests.post(f"{url}/books/{books[5][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 4,
    }
res = requests.post(f"{url}/books/{books[6][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[10][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[11][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[12][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[13][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[14][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[10][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[11][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[12][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[13][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[14][0]}/review/add", headers=headers, json=payload)


data = {
        "username": "caravanman",
        "firstName": "Jack",
        "lastName": "Camper",
        "email": "j@c.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[15][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[16][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[17][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[18][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[19][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[15][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[16][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[17][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[18][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[19][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "ainsy",
        "firstName": "Will",
        "lastName": "Ainsworth",
        "email": "w@a.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[15][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[16][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[17][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[18][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[19][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[15][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[16][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[17][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[18][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[19][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "tleeee",
        "firstName": "Tory",
        "lastName": "Leesworth",
        "email": "t@l.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[15][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[16][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[17][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[18][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[19][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[15][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[16][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[17][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[18][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[19][0]}/review/add", headers=headers, json=payload)


data = {
        "username": "bigman2",
        "firstName": "Jason",
        "lastName": "Biggs",
        "email": "j@b.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 3,
    }
#res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[15][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[16][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[17][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[18][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[19][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[15][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[16][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[17][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[18][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[19][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[10][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[11][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[12][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[13][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[14][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[10][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 2,
    }
res = requests.post(f"{url}/books/{books[11][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{books[12][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[13][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[14][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[8][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[8][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "holden4eva",
        "firstName": "Brock",
        "lastName": "Teemar",
        "email": "b@t.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[15][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[16][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[17][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[18][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[19][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[15][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[16][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[17][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[18][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[19][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[8][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[8][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "arrow555",
        "firstName": "Gary",
        "lastName": "Bowman",
        "email": "g@b.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[15][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[16][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[17][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[18][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[19][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[15][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[16][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[17][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[18][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[19][0]}/review/add", headers=headers, json=payload)


data = {
        "username": "aims321",
        "firstName": "Amy",
        "lastName": "Trove",
        "email": "a@t.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 3,
    }
#res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[15][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[16][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[17][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[18][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[19][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[15][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[16][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[17][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[18][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[19][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[10][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[11][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[12][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[13][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[14][0]}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{books[10][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 2,
    }
res = requests.post(f"{url}/books/{books[11][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{books[12][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 4,
    }
res = requests.post(f"{url}/books/{books[13][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[14][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[8][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[8][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "yeahbuddy",
        "firstName": "Ronnie",
        "lastName": "C",
        "email": "a@z.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
payload = {
        "title": "harry"
    }
res = requests.post(f"{url}/search", json=payload, headers=headers)
harry = res.json()[1]["bookId"]
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{books[9][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[9][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[7][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[7][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "awesome111",
        "firstName": "Lauren",
        "lastName": "Taylor",
        "email": "y@t.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
payload = {
        "title": "harry"
    }
res = requests.post(f"{url}/search", json=payload, headers=headers)
harry = res.json()[1]["bookId"]
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{books[9][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[9][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[7][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[7][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "yooper",
        "firstName": "Lauren",
        "lastName": "Taylor",
        "email": "y@q.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
payload = {
        "title": "harry"
    }
res = requests.post(f"{url}/search", json=payload, headers=headers)
harry = res.json()[1]["bookId"]
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{books[9][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[9][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[7][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[7][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "teemiller",
        "firstName": "Lauren",
        "lastName": "Taylor",
        "email": "t@t.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
payload = {
        "title": "harry"
    }
res = requests.post(f"{url}/search", json=payload, headers=headers)
harry = res.json()[1]["bookId"]
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{books[9][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[9][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[7][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[7][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "terry",
        "firstName": "Lauren",
        "lastName": "Taylor",
        "email": "r@e.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
payload = {
        "title": "harry"
    }
res = requests.post(f"{url}/search", json=payload, headers=headers)
harry = res.json()[1]["bookId"]
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{books[9][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[9][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[7][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[7][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "smallarms",
        "firstName": "Lauren",
        "lastName": "Taylor",
        "email": "s@q.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
payload = {
        "title": "harry"
    }
res = requests.post(f"{url}/search", json=payload, headers=headers)
harry = res.json()[1]["bookId"]
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{books[9][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[9][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[7][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[7][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "tools",
        "firstName": "Lauren",
        "lastName": "Taylor",
        "email": "t@o.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
payload = {
        "title": "harry"
    }
res = requests.post(f"{url}/search", json=payload, headers=headers)
harry = res.json()[1]["bookId"]
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{books[9][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[9][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[7][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[7][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "roweer",
        "firstName": "Lauren",
        "lastName": "Taylor",
        "email": "r@er.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
payload = {
        "title": "harry"
    }
res = requests.post(f"{url}/search", json=payload, headers=headers)
harry = res.json()[1]["bookId"]
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{books[9][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[9][0]}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[7][0]}", headers=headers)
payload = {
        "rating": 5,
    }
res = requests.post(f"{url}/books/{books[7][0]}/review/add", headers=headers, json=payload)

data = {
        "username": "johnno",
        "firstName": "John",
        "lastName": "Smith",
        "email": "j@s.com",
        "password": "Aaaaaaaa1!"
    }
res = requests.post(f"{url}/register", json=data)
username = data['username']
headers = {
        "Authorization": f"Bearer {res.json()['token']}"
    }
res = requests.get(f"{url}/collections/user/{username}", json=data, headers=headers)
main = res.json()["collections"][0]['collectionID']
res = requests.post(f"{url}/collections/{main}/add/{harry}", headers=headers)
payload = {
        "rating": 0,
    }
res = requests.post(f"{url}/books/{harry}/review/add", headers=headers, json=payload)
res = requests.post(f"{url}/collections/{main}/add/{books[0][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[1][0]}", headers=headers)
res = requests.post(f"{url}/collections/{main}/add/{books[2][0]}", headers=headers)
payload = {
        "rating": 3,
    }
res = requests.post(f"{url}/books/{books[0][0]}/review/add", headers=headers, json=payload)
payload = {
        "rating": 4,
    }
res = requests.post(f"{url}/books/{books[1][0]}/review/add", headers=headers, json=payload)

res = requests.post(f"{url}/users/follow/{'lauren92'}", headers=headers)
res = requests.post(f"{url}/users/follow/{'aBrowne'}", headers=headers)
res = requests.post(f"{url}/users/follow/{'goldie95'}", headers=headers)
res = requests.post(f"{url}/users/follow/{'yeahbuddy'}", headers=headers)
res = requests.post(f"{url}/users/follow/{'awesome111'}", headers=headers)
res = requests.post(f"{url}/users/follow/{'yooper'}", headers=headers)
res = requests.post(f"{url}/users/follow/{'teemiller'}", headers=headers)
res = requests.post(f"{url}/users/follow/{'terry'}", headers=headers)
#res = requests.post(f"{url}/users/follow/{'bigman2'}", headers=headers)
#res = requests.post(f"{url}/users/follow/{'aims321'}", headers=headers)

################################################################################

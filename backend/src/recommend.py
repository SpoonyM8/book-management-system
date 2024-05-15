import sqlite3
from ..config import db
from .error import InputError, DatabaseError, AccessError
from datetime import datetime, timedelta

def recommend(username, reqJson, bookID):
    # Flags are true/false values
    follows = reqJson["follows"]
    genre = reqJson["genre"]
    similar = reqJson["similar"]

    recommendations = []

    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        cur.execute(f"""select genre from Books
where bookID = "{bookID}";""")
        bookGenre = cur.fetchone()[0]

        users = []
        #if follows and not genre:
        if follows:
            cur.execute(f"""select username2 from Follows f;""")
            users = [f[0] for f in cur.fetchall()]
        elif follows and genre:
            cur.execute(f"""select username2 from Follows f
inner join Reviews r on r.username=f.username2
inner join Books b on b.bookID = r.bookID
where f.username1 = "{username}"
and r.bookID = "{bookID}"
and b.genre = "{bookGenre}";""")
            users = [f[0] for f in cur.fetchall()]
        
        if not follows or len(users) == 0:
            if not genre:
                cur.execute(f"""select username from Reviews
where bookID = "{bookID}"
and username != "{username}";""")
                users = [f[0] for f in cur.fetchall()]
                print("here")
            else:
                cur.execute(f"""select r.username from Reviews r
inner join Books b on b.bookID = r.bookID
where r.bookID = "{bookID}"
and r.username != "{username}"
and b.genre = "{bookGenre}";""")
                users = [f[0] for f in cur.fetchall()]
                
        if not users and not genre:
            return currPopular(username)
        elif not users and genre:
            cur.execute(f"""select bookID, title, author, coverImage from Books
where genre = "{bookGenre}"
and bookID not in (select a.bookID from hasRead a where username="{username}")
order by numRead
limit 5;""")
            tuples = cur.fetchall()
            for tuple in tuples:
                recommend = {}
                recommend["bookID"] = tuple[0]
                recommend["title"] = tuple[1]
                recommend["author"] = tuple[2]
                recommend["coverImage"] = tuple[3]
                recommendations.append(recommend)
            return {"recommend": recommendations}

        weights = {}
        if similar:
            temp = {}
            for user in users:
                cur.executescript(f"""drop view if exists ReviewA;
create view ReviewA as 
select rating, bookID from Reviews
where username = "{username}";
drop view if exists ReviewB;
create view ReviewB as 
select rating, bookID from Reviews
where username = "{user}";""")
                cur.execute(f"""select abs(rA.rating - rB.rating) as rDiff from ReviewA rA
inner join ReviewB rB on rB.bookID = rA.bookID;""")
                diffs = [f[0] for f in cur.fetchall()]
                if len(diffs) != 0:
                    temp[user] = sum(diffs) / len(diffs)
                else:
                    temp[user] = 5
            temp = sorted(temp.items(), key = lambda e: e[1])

            tempLen = len(temp)
            for idx, t in enumerate(temp):
                weights[t[0]] = tempLen - idx
        if not similar or len(weights) == 0:
            for user in users:
                weights[user] = 1
        
        print(weights)
        cur.executescript(f"""drop table if exists UserWeights;
create table UserWeights (
username varchar(36) not null,
weight integer not null,
primary key (username),
foreign key (username) references Users(username))""")
        for u, w in weights.items():
            cur.execute(f"""insert into UserWeights values ("{u}", {w});""")
        
        if not genre:
            cur.executescript(f"""drop view if exists GenreReviews;
create view GenreReviews as
select * from Reviews
where bookID != "{bookID}";""")
        else:
            cur.executescript(f"""drop view if exists GenreReviews;
create view GenreReviews as
select * from Reviews r
inner join Books b on b.bookID = r.bookID
where b.genre = "{bookGenre}"
and b.bookID != "{bookID}";""")
        
        cur.execute(f"""select r.bookID, b.title, b.author, b.coverImage, avg(r.rating * w.weight) as avgwrating from GenreReviews r
inner join UserWeights w on w.username = r.username
inner join Books b on b.bookID = r.bookID
where r.bookID not in (select a.bookID from hasRead a where username="{username}")
group by r.bookID
order by avgwrating desc, b.numRead desc
limit 5;""")
        tuples = cur.fetchall()
        for tuple in tuples:
            recommend = {}
            recommend["bookID"] = tuple[0]
            recommend["title"] = tuple[1]
            recommend["author"] = tuple[2]
            recommend["coverImage"] = tuple[3]
            recommendations.append(recommend)
        
        if len(recommendations) < 5:
            prevDate = datetime.now() - timedelta(days=30)
            if not genre:
                cur.execute(f"""select b.bookID, avg(r.rating) as avg, b.title, b.coverImage from Books b
inner join Reviews r on r.bookID = b.bookID
where r.timeAdded > "{prevDate}"
and b.bookID not in (select a.bookID from hasRead a where username="{username}")
group by b.bookID
order by avg desc, b.numRead desc;""")
            else:
                cur.execute(f"""select b.bookID, avg(r.rating) as avg, b.title, b.coverImage from Books b
inner join Reviews r on r.bookID = b.bookID
where r.timeAdded > "{prevDate}"
and b.bookID not in (select a.bookID from hasRead a where username="{username}")
and b.genre = "{bookGenre}"
group by b.bookID
order by avg desc, b.numRead desc;""")
            tuples = cur.fetchall()
            existing = [r["bookID"] for r in recommendations]

            for tuple in tuples:
                if tuple[0] in existing:
                    continue
                recommend = {}
                recommend["bookID"] = tuple[0]
                recommend["title"] = tuple[1]
                recommend["author"] = tuple[2]
                recommend["coverImage"] = tuple[3]
                recommendations.append(recommend)
                existing.append(tuple[0])
                if len(recommendations) >= 5:
                    break
            
        if len(recommendations) < 5:
            if not genre:
                cur.execute(f"""select bookID, title, author, coverImage from Books
where bookID not in (select a.bookID from hasRead a where username="{username}")
order by numRead desc
limit 5;""")
            else:
                cur.execute(f"""select bookID, title, author, coverImage from Books
where bookID not in (select a.bookID from hasRead a where username="{username}")
and genre = "{bookGenre}"
order by numRead desc
limit 5;""")
            tuples = cur.fetchall()
            for tuple in tuples:
                if tuple[0] in existing:
                    continue
                recommend = {}
                recommend["bookID"] = tuple[0]
                recommend["title"] = tuple[1]
                recommend["author"] = tuple[2]
                recommend["coverImage"] = tuple[3]
                recommendations.append(recommend)
                existing.append(tuple[0])
                if len(recommendations) >= 5:
                    break

    except sqlite3.Error as e:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()

    return {"recommend": recommendations}

def currPopular(username):
    recommendations = []
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        prevDate = datetime.now() - timedelta(days=30)
        cur.execute(f"""select b.bookID, avg(r.rating) as avg, b.title, b.coverImage from Books b
inner join Reviews r on r.bookID = b.bookID
where r.timeAdded > "{prevDate}"
and b.bookID not in (select a.bookID from hasRead a where username="{username}")
group by b.bookID
order by avg desc, b.numRead desc
limit 5;""")           
        tuples = cur.fetchall()
        if not tuples or tuples[0][0] == None:
            cur.execute(f"""select bookID, title, author, coverImage from Books
where bookID not in (select a.bookID from hasRead a where username="{username}")
order by numRead desc
limit 5;""")
            tuples = cur.fetchall()
        
        for tuple in tuples:
            recommend = {}
            recommend["bookID"] = tuple[0]
            recommend["title"] = tuple[1]
            recommend["author"] = tuple[2]
            recommend["coverImage"] = tuple[3]
            recommendations.append(recommend)

    except sqlite3.Error as e:
        raise DatabaseError(description="database error")
    finally:
        cur.close()
        conn.close()
    
    return {"recommend": recommendations}


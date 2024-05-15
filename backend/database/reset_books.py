import pandas as pd
import sqlite3
from uuid import uuid4
from random import randint

def reset_books():
    df = pd.read_csv("backend/database/book_data.csv", dtype="unicode")
    df.columns = ['row', 'title', 'author', 'yearPublished', 'publisher', 'img']

    conn = sqlite3.connect("backend/database/database.db")
    cur = conn.cursor()
    cur.execute("""delete from Books;""")
    genres = ["Crime", "Romance", "Science fiction", "Thriller", "Fantasy", "Mystery", "Horror", "Historical fiction"]
    count = 0
    for idx, row in df.iterrows():
        if count > 50000:
            break
        cur.execute("""insert into Books values (?,?,?,?,?,?,?,?,?,?)""", (str(uuid4()), row['title'], row['author'], row['yearPublished'], row['publisher'], row['img'], 0, 0.0, 0, genres[randint(0, len(genres)-1)]))
        count += 1
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    reset_books()

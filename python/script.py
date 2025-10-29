import sqlite3
import csv
import uvicorn
from fastapi import FastAPI
con = sqlite3.connect('movies.db')

cur = con.cursor()

# movies
if cur.execute("SELECT name FROM sqlite_master WHERE name='movies'").fetchone() is None:
    cur.execute('''CREATE TABLE movies(mID, Title, Genres)''')
    file = open('database/movies.csv', 'r', encoding='utf-8')
    reader = csv.reader(file)
    data = []
    for row in reader:
        data.append(row)
    cur.executemany('''Insert into movies(mID, Title, Genres) values (?,?,?)''', data)
    con.commit()


### links
if cur.execute("SELECT name FROM sqlite_master WHERE name='links'").fetchone() is None:
    cur.execute('''CREATE TABLE links(mID, imdbID, tmdbID)''')
    file = open('database/links.csv', 'r', encoding='utf-8')
    reader = csv.reader(file)
    data = []
    for row in reader:
        data.append(row)
    cur.executemany('''Insert into links(mID, imdbID, tmdbID) values (?,?,?)''', data)
    con.commit()

#ratings

if cur.execute("SELECT name FROM sqlite_master WHERE name='ratings'").fetchone() is None:
    cur.execute('''CREATE TABLE ratings(uID, mID, rating, timestamp)''')

    file = open('database/ratings.csv', 'r', encoding='utf-8')
    reader = csv.reader(file)
    data = []
    for row in reader:
        data.append(row)
    cur.executemany('''Insert into ratings(uID, mID, rating, timestamp) values (?,?,?,?)''', data)
    con.commit()

#tags

if cur.execute("SELECT name FROM sqlite_master WHERE name='tags'").fetchone() is None:
    cur.execute('''CREATE TABLE tags(uID, mID,tag, timestamp)''')
    file = open('database/tags.csv', 'r', encoding='utf-8')
    reader = csv.reader(file)
    data = []
    for row in reader:
        data.append(row)
    cur.executemany('''Insert into tags(uID, mID,tag, timestamp) values (?,?,?,?)''', data)
    con.commit()

app = FastAPI()

class Movie:
    def __init__(self, id, title, genres):
        self.id = id
        self.title = title
        self.genres = genres

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/movies")
def read_item():
    return Movies

file = open("database/movies.csv", "r", encoding="utf-8")
query = [list(row) for row in cur.execute('''SELECT * FROM movies''').fetchall()]
Movies = []
for line in query:
    if line[0].isdigit():
        Movies.append(Movie(line[0], line[1], line[2]).__dict__)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


con.close()
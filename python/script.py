import sqlite3
import csv
import uvicorn
from fastapi import FastAPI, HTTPException
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

class Rating:
    def __init__(self, uID, mID, rating, timestamp):
        self.uID = uID
        self.mID = mID
        self.rating = rating
        self.timestamp = timestamp

class Tag:
    def __init__(self, uID, mID, tag, timestamp):
        self.uID = uID
        self.mID = mID
        self.tag = tag
        self.timestamp = timestamp

class Link:
    def __init__(self, mID, imdbID, tmdbID):
        self.mID = mID
        self.imdbID = imdbID
        self.tmdbID = tmdbID
file = open("database/movies.csv", "r", encoding="utf-8")
query = [list(row) for row in cur.execute('''SELECT * FROM movies''').fetchall()]
Movies = []
for line in query:
    if line[0].isdigit():
        Movies.append(Movie(line[0], line[1], line[2]).__dict__)

file = open("database/ratings.csv", "r", encoding="utf-8")
query = [list(row) for row in cur.execute('''SELECT * FROM ratings''').fetchall()]
Ratings = []
for line in query:
    if line[0].isdigit():
        Ratings.append(Rating(line[0], line[1], line[2], line[3]).__dict__)

file = open("database/links.csv", "r", encoding="utf-8")
query = [list(row) for row in cur.execute('''SELECT * FROM links''').fetchall()]
Links = []
for line in query:
    if line[0].isdigit():
        Links.append(Link(line[0], line[1], line[2]).__dict__)


file = open("database/tags.csv", "r", encoding="utf-8")
query = [list(row) for row in cur.execute('''SELECT * FROM tags''').fetchall()]
Tags = []
for line in query:
    if line[0].isdigit():
        Tags.append(Tag(line[0], line[1], line[2], line[3]).__dict__)

@app.get("/")
def read_root():
    return {"Hello" : "World"}

@app.get("/movies")
def read_item():
    return Movies

@app.post("/movies")
def add_item(Data: Movie):
    id = Data.id
    title = Data.title
    genres = Data.genres
    if cur.execute("""Select * from movies where id = ?""", (id,)).fetchone() is None:
        cur.execute("""INSERT INTO movies(mID, Title, Genres) values (?,?,?)""",[id, title, genres])
        return {"status": "movie added"}
    else:
        raise HTTPException(status_code=401, detail="Invalid ID")

@app.read("/movies/{mID}")
def read_item(mID: int):
    query = cur.execute("""SELECT * FROM movies where mID = ?""", [mID]).fetchone()
    if query is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    else:
        return Movie(query[0], query[1], query[2])

@app.put("/movies")
def update_item(Data: Movie):
    mID = Data.id
    title = Data.title
    genres = Data.genres
    if cur.execute("""SELECT * FROM movies where mID = ?""", [mID]).fetchone():
        cur.execute("UPDATE movies set Title = ?,Genres = ? where id = ?", [title, genres, mID])
        return {"status": "movie updated"}
    else:
        raise HTTPException(status_code=404, detail="Movie not found")

@app.delete("/movies/{mID}")
def delete_item(mID: int):
    if cur.execute("""SELECT * FROM movies where mID = ?""", [mID]).fetchone():
        cur.execute("""DELETE FROM movies where mID = ?""", [mID])




@app.get("/ratings")
def read_item():
    return Ratings

@app.post("/ratings")
def add_item(Data: Rating):
    uid = Data.uID
    mid = Data.mID
    rating = Data.rating
    timestamp = Data.timestamp

    if cur.execute("""Select * from movies where id = ?""", (mid,)).fetchone():
        cur.execute("""INSERT INTO ratings(uID, mID, rating, timestamp) values (?,?,?,?)""",[uid, mid, rating, timestamp])
        return {"status": "rating added"}
    else:
        raise HTTPException(status_code=401, detail="movie ID does not exist")

@app.get("/links")
def read_item():
    return Links
@app.post("/links")
def add_item(Data: Link):
    mID = Data.mID
    imdbID = Data.imdbID
    tmdbID = Data.tmdbID

    if cur.execute("""Select * from movies where id = ?""", (mID,)).fetchone():
        cur.execute("""INSERT INTO ratings(mID, imdbID, tmdbID) values (?, ?, ?)""", [mID, imdbID, tmdbID])
        return {"status": "Link added"}
    else:
        raise HTTPException(status_code=401, detail="movie ID does not exist")

@app.get("/tags")
def read_item():
    return Tags

@app.post("/tags")
def add_item(Data: Tag):
    uID = Data.uID
    mID = Data.mID
    tag = Data.tag
    timestamp = Data.timestamp

    if cur.execute("""Select * from movies where id = ?""", (mID,)).fetchone():
        cur.execute("""INSERT INTO ratings(uID, mID, tag, timestamp) values (?, ?, ?)""", [uID, mID, tag, timestamp])
        return {"status": "Tag added"}
    else:
        raise HTTPException(status_code=401, detail="movie ID does not exist")



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


con.close()
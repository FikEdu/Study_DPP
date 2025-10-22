import sqlite3
import csv
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
if cur.execute('''select count(*) from movies''').fetchone()[0]>0:
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
if cur.execute('''select count(*) from links''').fetchone()[0]>0:
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
if cur.execute('''select count(*) from ratings''').fetchone()[0]>0:
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
if cur.execute('''select count(*) from tags''').fetchone()[0]>0:
    cur.executemany('''Insert into tags(uID, mID,tag, timestamp) values (?,?,?,?)''', data)
    con.commit()

con.close()
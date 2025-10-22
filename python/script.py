import csv
import uvicorn
from fastapi import FastAPI

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
reader = csv.reader(file)
Movies = []
for line in reader:
    if line[0].isdigit():
        Movies.append(Movie(line[0], line[1], line[2]).__dict__)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

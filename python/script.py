import uvicorn
from fastapi import FastAPI, HTTPException
import cv2
import img_read
import numpy as np
import urllib.request
from pygments.formatters import img

from python.img_read import count_ppl_on_img

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/analyze_img")
async def analyze_img(link: str):
    return {'Amount':count_ppl_on_img(link)}

@app.get("/analyze_img")
async def analyze_img(link: str):
    return {'Amount':count_ppl_on_img(link)}




if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
from fastapi import FastAPI, Request
from transformers import pipeline
import sqlite3
import pandas as pd

app = FastAPI()
sentiment_pipeline = pipeline("sentiment-analysis")

# Init DB
conn = sqlite3.connect('sentiments.db')
conn.execute('CREATE TABLE IF NOT EXISTS reviews (product TEXT, review TEXT, label TEXT, score REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')

@app.post("/webhook/review")
async def handle_review(request: Request):
    data = await request.json()
    result = sentiment_pipeline(data['review'])[0]
    conn.execute("INSERT INTO reviews VALUES (?, ?, ?, ?, datetime('now'))", 
                 (data['product'], data['review'], result['label'], result['score']))
    conn.commit()
    return {"status": "analyzed", "sentiment": result['label']}

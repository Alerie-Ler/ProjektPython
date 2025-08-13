from fastapi import FastAPI, HTTPException

from pydantic import BaseModel




import json

import requests

import sqlite3

app = FastAPI()


conn = sqlite3.connect("travel.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

class Trip(BaseModel):
    destination: str
    month: str
    price_pln: float

def initialize_database():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destination TEXT NOT NULL,
            month TEXT NOT NULL,
            price_pln REAL NOT NULL CHECK(price_pln >= 0)
        )
        """)
    conn.commit()

initialize_database()

def add_trip(destination, month, price_pln):
    try:
        cur.execute("INSERT INTO trips (destination, month, price) VALUES (?, ?, ?)",(destination, month, price_pln))
        conn.commit()
        return
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

def read_trips():
    try:
        cur.execute("SELECT * FROM trips")
        return cur.fetchall()
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

def read_trip(destination: str):
    try:
        cur.execute("SELECT * FROM trips WHERE destination = ?", (destination,))
        return cur.fetchone()
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")

@app.get("/currency")
def get_currency(currency_code: str):
    url = "https://api.nbp.pl/api/exchangerates/tables/A?format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rates = data[0]['rates']
        for rate in rates:
            if rate['code'].upper() == currency_code.upper():
                return rate['mid']
        raise HTTPException(status_code=400, detail=f"Unsupported currency code: {currency_code}")
    except requests.Timeout:
        raise HTTPException(status_code=400, detail="NBP API request timed out")
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"NBP API error: {str(e)}")

@app.get("/convert")
def convert_currency(pln: float, currency_code: str):
    if pln < 0:
        raise HTTPException(status_code=422, detail="pln amount must be non-negative")
    rate = get_currency(currency_code)
    converted = pln / rate
    return {
        "amount_pln": round(pln, 2),
        "currency": currency_code.upper(),
        "converted_amount": round(converted, 2)
    }



@app.get("/health")
def read_health():
    return {"status": "ok"}

if __name__ == '__main__':

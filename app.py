from fastapi import FastAPI, HTTPException

from pydantic import BaseModel




import json

import requests

import sqlite3

app = FastAPI()


conn = sqlite3.connect("travel.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

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

def add_trip(destination, month, price_pln):
    cur.execute("INSERT INTO trips (destination, month, price) VALUES (?, ?, ?)",(destination, month, price_pln))
    conn.commit()
    return

def read_trips():
    cur.execute("SELECT * FROM trips")
    return cur.fetchall()

def read_trip(destination: str):
    cur.execute("SELECT * FROM trips WHERE destination = ?", (destination,))
    return cur.fetchone()

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
        raise ValueError(f"Nieobsługiwany kod waluty: {currency_code}")
    except requests.RequestException as e:
        return HTTPException(status_code=500, detail=str(e))

@app.get("/convert")
def convert_currency(pln: float, currency_code: str):
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
    app.run(debug=True)

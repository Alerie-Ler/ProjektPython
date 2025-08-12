from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

import sqlite3

app = FastAPI()


conn = sqlite3.connect("travel.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination TEXT NOT NULL,
        month TEXT NOT NULL,
        price_pln REAL
    )
    """)
conn.commit()
conn.close()

def add_trip(destination: str, month: str, price: float):
    cur.execute("INSERT INTO trips (destination, month, price) VALUES (?, ?, ?)",("Greece", "May", 655))
    conn.commit()
    return

def read_trips():
    cur.execute("SELECT * FROM trips")
    return cur.fetchall()

def read_trip(destination: str):
    cur.execute("SELECT * FROM trips WHERE destination = ?", (destination,))
    return cur.fetchone()






@app.get("/health")
def read_health():
    return {"status": "ok"}

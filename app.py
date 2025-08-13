
from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, validator
from typing import Dict
import requests

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

import requests

import json

import sqlite3


app = FastAPI(title="Trips API", version="1.0.0")
class Trip(BaseModel):
    destination: str
    month: str
    price_pln: float
    @validator('destination', 'month')
    def check_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Pole nie może być puste')
        return v
    @validator('price_pln')
    def check_price(cls, v):
        if v < 0:
            raise ValueError('Cena musi być większa lub równa 0')
        return v
db: Dict[int, Trip] = {}
current_id = 1
def add_trip_to_db(trip: Trip) -> Dict:
    global current_id
    try:
        db[current_id] = trip
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Błąd bazy danych", "message": str(e)}
        )
    trip_data = trip.dict()
    trip_data["id"] = current_id
    current_id += 1
    return trip_data

def get_exchange_rate(currency: str) -> float:
    currency = currency.upper()
    if currency == "PLN":
        return 1.0
    url = f"https://api.nbp.pl/api/exchangerates/rates/A/{currency}/?format=json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail={"error": "Błąd API NBP", "message": f"Nie znaleziono kursu dla waluty {currency}"}
            )
        data = response.json()
        return data["rates"][0]["mid"]
    except requests.Timeout:
        raise HTTPException(
            status_code=400,
            detail={"error": "Błąd API NBP", "message": "Przekroczono czas oczekiwania na odpowiedź NBP"}
        )
    except requests.RequestException as e:
        raise HTTPException(
            status_code=400,
            detail={"error": "Błąd API NBP", "message": str(e)}
        )
@app.post("/trips", status_code=status.HTTP_201_CREATED)
def create_trip(trip: Trip):
    try:
        return add_trip_to_db(trip)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "Niepoprawne dane", "message": str(e)}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Błąd bazy danych", "message": str(e)}
        )
@app.get("/trips")
def list_trips(currency: str = Query("PLN", description="Kod waluty (np. PLN)")):
    rate = get_exchange_rate(currency)
    result = []
    for trip_id, trip in db.items():
        trip_data = trip.dict()
        trip_data["id"] = trip_id
        trip_data["price"] = round(trip_data["price_pln"] / rate, 2)
        trip_data["currency"] = currency.upper()
        result.append(trip_data)
    return result
@app.get("/trips/{destination}")
def get_trip(destination: str, currency: str = Query("PLN", description="Kod waluty (np. PLN)")):
    rate = get_exchange_rate(currency)
    for trip_id, trip in db.items():
        if trip.destination.lower() == destination.lower():
            trip_data = trip.dict()
            trip_data["id"] = trip_id
            trip_data["price"] = round(trip_data["price_pln"] / rate, 2)
            trip_data["currency"] = currency.upper()
            return trip_data
    raise HTTPException(
        status_code=404,
        detail={"error": "Brak wyników", "message": f"Nie znaleziono podróży do {destination}"}
    )
@app.get("/health")
def read_health():
    return {"status": "ok"}
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


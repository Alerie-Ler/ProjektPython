from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import Dict

app = FastAPI()

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
            raise ValueError('Cena musi byc większa lub równa 0')
        return v


@app.get("/health")
def read_health():
    return {"status": "ok"}


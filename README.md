# Trips API

## Spis treści

* [Opis projektu](#opis-projektu)
* [Wymagania](#wymagania)
* [Instalacja i uruchomienie](#instalacja-i-uruchomienie)
* [Endpointy API](#endpointy-api)
* [Przykłady wywołań curl](#przykłady-wywołań-curl)
* [Parametry](#parametry)
* [Ograniczenia projektu](#ograniczenia-projektu)

---

## Opis projektu

Trips API to prosty serwis RESTowy do zarządzania wycieczkami.
Obsługuje przechowywanie wycieczek w lokalnej bazie SQLite oraz konwersję cen wycieczek na różne waluty dzięki API Narodowego Banku Polskiego (NBP).

---

## Wymagania

* Python 3.8+
* FastAPI
* requests
* SQLite (wbudowany w Python)
* narzędzie do uruchamiania ASGI np. `uvicorn`

---

## Instalacja i uruchomienie

1. Sklonuj repozytorium lub skopiuj plik `main.py`.
2. Zainstaluj zależności:

```bash
pip install fastapi uvicorn requests
```

3. Uruchom serwer:

```bash
uvicorn main:app --reload
```

4. API dostępne jest pod adresem:
   `http://127.0.0.1:8000`

---

## Endpointy API

| Metoda | Ścieżka              | Opis                                            |
| ------ | -------------------- | ----------------------------------------------- |
| GET    | /health              | Sprawdzenie statusu serwera                     |
| POST   | /trips               | Dodanie nowej wycieczki                         |
| GET    | /trips               | Lista wszystkich wycieczek (z konwersją waluty) |
| GET    | /trips/{destination} | Pobranie wycieczki po celu (z konwersją waluty) |
| GET    | /currency            | Pobranie kursu waluty z NBP                     |
| GET    | /convert             | Przeliczenie kwoty PLN na podaną walutę         |

---

## Przykłady wywołań curl

### 1. Sprawdzenie statusu serwera

```bash
curl -X GET http://127.0.0.1:8000/health
```

**Odpowiedź:**

```json
{"status":"ok"}
```

---

### 2. Dodanie nowej wycieczki

```bash
curl -X POST http://127.0.0.1:8000/trips \
 -H "Content-Type: application/json" \
 -d '{"destination":"Paryż", "month":"Maj", "price_pln":1500.5}'
```

**Odpowiedź:**

```json
{
  "id": 1,
  "destination": "Paryż",
  "month": "Maj",
  "price_pln": 1500.5
}
```

---

### 3. Lista wycieczek w walucie EUR

```bash
curl -X GET "http://127.0.0.1:8000/trips?currency=EUR"
```

**Odpowiedź:**

```json
[
  {
    "id": 1,
    "destination": "Paryż",
    "month": "Maj",
    "price": 330.12,
    "currency": "EUR"
  }
]
```

---

### 4. Pobranie wycieczki do Paryża w PLN

```bash
curl -X GET "http://127.0.0.1:8000/trips/Paryż?currency=PLN"
```

**Odpowiedź:**

```json
{
  "id": 1,
  "destination": "Paryż",
  "month": "Maj",
  "price": 1500.5,
  "currency": "PLN"
}
```

---

### 5. Pobranie kursu waluty USD

```bash
curl -X GET "http://127.0.0.1:8000/currency?currency_code=USD"
```

**Odpowiedź:**

```json
3.95
```

---

### 6. Konwersja kwoty 1000 PLN na USD

```bash
curl -X GET "http://127.0.0.1:8000/convert?pln=1000&currency_code=USD"
```

**Odpowiedź:**

```json
{
  "amount_pln": 1000,
  "currency": "USD",
  "converted_amount": 253.16
}
```

---

## Parametry

* `currency` — kod waluty ISO 4217 (np. PLN, EUR, USD). Domyślnie `PLN`.
* `destination` — nazwa celu podróży (ciąg znaków).
* `month` — miesiąc wycieczki (ciąg znaków).
* `price_pln` — cena wycieczki w PLN (liczba zmiennoprzecinkowa, >=0).
* `pln` — kwota w złotówkach do konwersji (float, >=0).
* `currency_code` — kod waluty do konwersji (ISO 4217).

---

## Ograniczenia projektu

* Ceny przechowywane są tylko w PLN w bazie SQLite.
* Wyciek danych i błędy walidacji nie są w pełni zabezpieczone.
* Brak paginacji i filtrowania wyników.
* API NBP jest wykorzystywane bez cachowania, co może powodować spowolnienie.
* Wyszukiwanie wycieczki po `destination` jest czułe na wielkość liter.
* Brak autoryzacji i uwierzytelniania użytkowników.

---

Masz pytania lub chcesz rozbudować projekt? Chętnie pomogę!

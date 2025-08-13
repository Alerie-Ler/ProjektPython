# Travel API

Prosty serwer FastAPI do zarządzania ofertami wycieczek oraz konwersji walut na podstawie danych z API NBP.

---

## 1. Instrukcja uruchomienia

### Wymagania

- Python 3.8+
- pip

### Instalacja zależności

```bash
pip install fastapi uvicorn requests pydantic
````

### Uruchomienie serwera

```bash
uvicorn main:app --reload
```

Gdzie `main.py` to plik z kodem aplikacji (dostosuj nazwę pliku według własnej struktury).

### Baza danych

* Baza SQLite `travel.db` zostanie utworzona automatycznie przy pierwszym uruchomieniu serwera.
* Tabela `trips` zawiera kolumny: `id`, `destination`, `month`, `price_pln`.

---

## 2. API - Endpoints i parametry

### `/health` (GET)

Sprawdza, czy serwer działa.

**Odpowiedź:**

```json
{ "status": "ok" }
```

---

### `/trips` (GET)

Pobiera listę wszystkich wycieczek.

**Odpowiedź:**

```json
[
  {
    "id": 1,
    "destination": "Barcelona",
    "month": "July",
    "price_pln": 1500.0
  },
  ...
]
```

---

### `/trips` (POST)

Dodaje nową wycieczkę.

**Body (JSON):**

```json
{
  "destination": "Barcelona",
  "month": "July",
  "price_pln": 1500.0
}
```

**Walidacja:**

* `destination`: nie może być puste,
* `month`: nie może być puste,
* `price_pln`: liczba >= 0.

**Odpowiedź:**

```json
{ "message": "Trip added successfully" }
```

---

### `/trips/{destination}` (GET)

Pobiera wycieczkę po nazwie `destination`.

**Parametr URL:**
`destination` - nazwa miejsca docelowego (np. Barcelona)

**Odpowiedź:**

```json
{
  "id": 1,
  "destination": "Barcelona",
  "month": "July",
  "price_pln": 1500.0
}
```

---

### `/currency` (GET)

Pobiera aktualny kurs średni danej waluty względem PLN z API NBP.

**Parametry query:**
`currency_code` — kod waluty, np. `USD`, `EUR`, `GBP`.
Kody muszą być zgodne z listą NBP.

**Odpowiedź (float):**
Przykład: `4.5234`

---

### `/convert` (GET)

Konwertuje kwotę z PLN na podaną walutę.

**Parametry query:**

* `pln` (float): kwota w PLN (>= 0),
* `currency_code` (str): kod waluty docelowej.

**Odpowiedź:**

```json
{
  "amount_pln": 1000.0,
  "currency": "USD",
  "converted_amount": 225.45
}
```

---

## 3. Przykłady wywołań CURL

### Pobranie statusu zdrowia serwera

```bash
curl http://127.0.0.1:8000/health
```

---

### Dodanie nowej wycieczki

```bash
curl -X POST http://127.0.0.1:8000/trips \
-H "Content-Type: application/json" \
-d '{"destination":"Barcelona", "month":"July", "price_pln":1500}'
```

---

### Pobranie wszystkich wycieczek

```bash
curl http://127.0.0.1:8000/trips
```

---

### Pobranie wycieczki po nazwie

```bash
curl http://127.0.0.1:8000/trips/Barcelona
```

---

### Pobranie kursu waluty

```bash
curl "http://127.0.0.1:8000/currency?currency_code=USD"
```

---

### Konwersja PLN na inną walutę

```bash
curl "http://127.0.0.1:8000/convert?pln=1000&currency_code=USD"
```

---

## 4. Znane ograniczenia i uwagi

* Baza danych SQLite jest prosta i nie jest przystosowana do środowisk produkcyjnych z dużą liczbą użytkowników i zapytań.
* Walidacja kodów walut jest zależna od aktualnych danych z API NBP — mogą wystąpić ograniczenia lub zmiany w liście walut.
* Timeout dla zapytań do API NBP jest ustawiony na 5 sekund.
* Nie ma autoryzacji użytkowników — API jest otwarte.
* Pole `month` przyjmuję dowolny tekst — brak walidacji, czy to rzeczywiście nazwa miesiąca.
* Brak paginacji dla endpointu `/trips`.

---

## 5. Kontakt / wsparcie

W razie pytań lub problemów, proszę o kontakt.

---

# Powodzenia! 🚀



Chcesz, mogę wygenerować plik README.md lub pomóc z automatycznymi testami?
```

Cel: w parach tworzycie proste API do zarządzania ofertami podróży.

    Dane trzymane w SQLite w jednej tabeli trips: id, destination (TEXT), month (TEXT), price_pln (REAL).
    API pozwala:
        dodać nową ofertę (POST /trips),
        pobrać wszystkie oferty (GET /trips),
        pobrać oferty do danego miejsca (GET /trips/{destination}),
        w każdym z widoków pobrać ceny w innej walucie (?currency=EUR|USD|...) – kurs z API NBP.
    Wszystko w jednym pliku Pythona.

Stos technologiczny: Python 3.10+, FastAPI, Uvicorn, SQLite (sqlite3), requests.
Podział ról:

    Dev A – obsługa bazy danych, logika przeliczania walut, komunikacja z API NBP.
    Dev B – definicja endpointów API, walidacje danych wejściowych, format odpowiedzi, dokumentacja.

# Instalacja Backendu

# 1. Sklonuj repozytorium Bikeatize

# 2. Stwórz wirtualne środowisko i zainstaluj zależności

# 3. Skonfiguruj zmienne środowiskowe
W głównym katologu stwórz plik .env <br>
Edytuj .env dodajac wlasne wartości:<br>

<strong>Klucz do podpisywania JWT:</strong><br>
ECRET_KEY=zmien_mnie_na_sekretny_klucz<br>

<strong>Połączenie z bazą danych (zastąp danymi swojego MySQL)</strong><br>
DATABASE_URL=mysql+asyncmy://user:password@localhost:3306/bikeatize_db

# 4. Migracja bazy danych (Alembic)

Zainstaluj Alembic i uruchom migracje:<br>
**bash:** alembic upgrade head &nbsp; # Tworzy tabelę w bazie danych

# 5. Uruchom aplikację

uvicorn backend.main:app --reload <br>
API powinno działać na: http://127.0.0.1:8000 (SwaggerUI)

# 6. Lista Endpointów API:
**Autoryzacja użytkownika:**
<ul>
    <li>POST /login > Logowanie użytkownika</li>
    <li>POST /register > Rejestracja nowego użytkownika</li>
    <li>POST /logout > Wylogowanie</li>
    <li>POST /refresh > Odświeżanie tokena JWT</li>
</ul>

**Obsługa tras rowerowych:**

<ul>
    <li>POST /start_trip/{user_id} → Rozpoczęcie trasy</li>
    <li>POST /update_location/{trip_id}?latitude=XX&longitude=XX → Aktualizacja lokalizacji</li>
    <li>POST /stop_trip/{trip_id} → Zakończenie trasy</li>
    <li>GET /trip_history/{user_id} → Historia tras</li>
</ul>

# 7. Uwagi

- Jeśli masz problem z .env, upewnij się, że znajduje się w katalogu głównym repo.
- Jeśli używasz Pythona 3.12+ i masz problem z asyncmy, możesz użyć aiomysql.




# Instalacja Backendu

# 1. Sklonuj repozytorium Bikeatize

# 2. Stwórz wirtualne środowisko i zainstaluj zależności

# 3. Skonfiguruj zmienne środowiskowe
W katalogu głównym stwórz plik .env <br>
Edytuj .env dodajac wlasne wartości:<br>

DATABASE_URL=mysql+asyncmy://user:password@localhost:3306/bikeatize<br>
SECRET_KEY=super_secret_key <br>

# 5. Uruchom aplikację

uvicorn backend.main:app --reload <br>
API powinno działać na: http://127.0.0.1:8000

# 6. Lista Endpointów API:
<ul>
    <li>POST /login > Logowanie użytkownika</li>
    <li>POST /register > Rejestracja nowego użytkownika</li>
    <li>POST /logout > Wylogowanie</li>
    <li>POST /refresh > Odświeżanie tokena JWT</li>
</ul>

# 7. Uwagi

Jeśli masz problem z .env, upewnij się, że znajduje się w katalogu głównym repo




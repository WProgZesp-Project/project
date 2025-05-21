# PdfApp

PdfApp to aplikacja Django służąca do obsługi plików Pdf. Będzie umożliwiać manipulowanie formatem plików, operacje na plikach oraz kompresje.

## Wymagania

- Python 3.x

## Instrukcja uruchomienia

### 1. Klonowanie repozytorium

```bash
git clone https://github.com/WProgZesp-Project/project.git
cd project
```
### 2. Tworzenie wirtualnego środowiska

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalowanie zależności

```bash
pip install -r requirements.txt
```

### 4. Lokalna baza danych
Aby lokalnie postawić kontener PostgreSQL, można użyć Dockera. Upewnij się, że Docker jest zainstalowany i uruchomiony na twoim systemie.
```bash
docker run --name pdf-postgres     -e POSTGRES_DB=pdfdb     -e POSTGRES_USER=pdfuser     -e POSTGRES_PASSWORD=pdfpass     -p 5432:5432     -d postgres:14
```
Następnie, aby połączyć się z bazą danych PostgreSQL z aplikacji Django, należy użyć lokalnych zmiennych środowiskowych:
```
POSTGRES_DB=pdfdb
POSTGRES_USER=pdfuser
POSTGRES_PASSWORD=pdfpass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

### 5. Tworzenie migracji

```bash
cd pdfapp
python manage.py migrate
```

### 6. Uruchomienie serwera
```bash
python manage.py runserver
```

### 7. Obsługa email
Aby obsługa email działała, należy dodać zmienne środowiskowe:
```
EMAIL=progzesppdf@gmail.com
EMAIL_PASS=tztgdqxdykuppjop
```

### 8. Lokalne testowanie
Aby nie musieć za każdą rejestracją potwierdzać maila, należy ustawić zmienną środowiskową:
```
TEST=true
```

Po uruchomieniu aplikacja będzie dostępna pod adresem http://127.0.0.1:8000/.


## Endpoints

### Frontend
`/remove-password`

### Backend
`/api/merge-pdfs `- endpoint do mergowania plików pdf  
`/api/remove-password` - endpoint do usuwania hasła dla pliku pdf   


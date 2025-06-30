# PdfApp

PdfApp to aplikacja Django służąca do obsługi plików Pdf. Będzie umożliwiać manipulowanie formatem plików, operacje na plikach oraz kompresje.

## Wymagania

- Python 3.10

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
Aby lokalnie postawić kontener PostgreSQL, można użyć Dockera. Upewnij się, że Docker jest zainstalowany i uruchomiony na twoim systemie. W razie problemów z połączniem sprawdź, czy instancja postgres nie jest uruchomiona lokalnie - nie może być jeśli chcesz połączyć się przez dockera.
```bash
docker run --name pdf-postgres     -e POSTGRES_DB=pdfdb     -e POSTGRES_USER=pdfuser     -e POSTGRES_PASSWORD=pdfpass     -p 5432:5432     -d postgres:14
```

### 5. Ustawienie zmiennych środowiskowych
W project/ należy stworzyć plik .env ze zmiennymi SECRET_KEY, AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY. Dodatkowo, aby obsługa email działała, należy dodać zmienne środowiskowe:
```
EMAIL=progzesppdf@gmail.com
EMAIL_PASS=tztgdqxdykuppjop
```
Aby nie musieć za każdą rejestracją potwierdzać maila, należy ustawić zmienną środowiskową:
```
TEST=true
```

### 6. Tworzenie migracji

```bash
cd pdfapp
python manage.py migrate
```

### 7. Uruchomienie serwera
```bash
python manage.py runserver
```
Po uruchomieniu aplikacja będzie dostępna pod adresem http://127.0.0.1:8000/.

## Endpointy

### Frontend
`/remove-password`

### Backend
`/api/merge-pdfs `- endpoint do mergowania plików pdf  
`/api/remove-password` - endpoint do usuwania hasła dla pliku pdf   
`/api/remove-pages` - endpoint do usuwania stron z pliku pdf   

### 9. Ekstrakcja stron
Estrakcja wybranych stron z pliku pdf

url: `api/extract-pages`

method: POST

body: file: plik, pages: strony, np. 1,3,5-7,9
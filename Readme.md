# PdfApp

PdfApp to aplikacja Django służąca do obsługi plików Pdf. Będzie umożliwiać manipulowanie formatem plików, operacje na plikach oraz kompresje.

## Wymagania

- Python 3.x
- MongoDB Community Server

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

### 4. Tworzenie migracji

```bash
cd pdfapp
python manage.py migrate
```

### 5. Uruchomienie serwera
```bash
python manage.py runserver
```

Po uruchomieniu aplikacja będzie dostępna pod adresem http://127.0.0.1:8000/.

# [www.tojeto.rs](https://www.tojeto.rs/)

## Django real estate website - Setup Guide

### Prerequisites
- Python 3 installed
- pip (Python package manager) installed

### Steps to Run the Django Website

#### 1. Create a Virtual Environment
It is recommended to use a virtual environment for the project to manage dependencies.
```bash
python3 -m venv .myvenv
```

#### 2. Activate the Virtual Environment
#### On macOS/Linux:
```bash
source .myvenv/bin/activate
```
#### On Windows (CMD):
```cmd
.myvenv\Scripts\activate
```
#### On Windows (PowerShell):
```powershell
.myvenv\Scripts\Activate.ps1
```

#### 3. Install Django
Once the virtual environment is activated, install Django:
```bash
pip install django
```

#### 4. Apply Migrations
Run database migrations to set up the database schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. Start the Django Development Server
Run the Django server locally:
```bash
python manage.py runserver
```
By default, the website will be available at:
```
http://127.0.0.1:8000/
```

#### 6. (Optional) Create a Superuser
If you need to access the Django Admin panel, create a superuser:
```bash
python manage.py createsuperuser
```
Follow the prompts to set up a username and password.

#### 7. (Optional) Run Server on a Specific IP/Port
If you need to access the server from another device or change the port:
```bash
python manage.py runserver 0.0.0.0:8000
```

#### 8. (Optional) Collect Static Files
If the project has static files (CSS, JS, images), run:
```bash
python manage.py collectstatic
```

#### 9. Access the Website
- Open **`http://127.0.0.1:8000/`** in your browser.
- If using Django Admin, go to **`http://127.0.0.1:8000/admin/`** and log in with your superuser credentials.

---

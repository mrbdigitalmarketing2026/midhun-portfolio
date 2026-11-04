# Midhun Balachandran — Personal Portfolio

A Django starter project for a premium dark black-and-purple personal portfolio.

## 1. Create and activate a virtual environment (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:
```bat
.venv\Scripts\activate.bat
```

## 2. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Run database migrations and create an admin user

```powershell
python manage.py migrate
python manage.py createsuperuser
```

## 4. Start the development server

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.
Admin: http://127.0.0.1:8000/admin/

## 5. Add your photograph

Copy your professional photo into:
`static/images/midhun-profile.jpg`

Use a clear, high-resolution portrait. The homepage has a styled placeholder until this file is added.

## Notes

- This is a fresh, standalone project. It does not connect to or modify any other app or database.
- SQLite is used for local development.
- Before public deployment, set a secure `SECRET_KEY`, `DEBUG=False`, allowed hosts, HTTPS, and a production database.
- Replace the sample email/social links and project placeholders with confirmed details before publishing.

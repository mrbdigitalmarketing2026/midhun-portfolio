# Midhun Balachandran — Personal Portfolio

**Digital Marketer | Video Creator | Entrepreneur**

Welcome to my personal portfolio repository. This project showcases my professional experience, creative work, digital marketing services, technical skills and business projects.

I am the Founder & Managing Director of **MRB Digital Marketing & Advertising**, based in Palakkad, Kerala, India.

## 🌐 Portfolio Overview

A premium, responsive personal portfolio website developed using Django, Python and modern frontend technologies.

The website is designed to introduce my professional journey, showcase selected projects and help potential clients connect with me.

## ✨ Website Features

- Premium dark black and purple design.
- Professional introduction and About section.
- Digital marketing and creative service showcase.
- Selected client projects and portfolio work.
- Skills and tools section.
- Contact and enquiry form.
- Django Admin enquiry management dashboard.
- Client priority and lead-source tracking.
- Follow-up management and activity history.
- Google Sheets enquiry integration.
- Email notifications for new enquiries.
- Responsive website layout.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| HTML5 | Website structure |
| CSS3 | Styling and responsive design |
| JavaScript | Frontend interactions |
| SQLite | Local development database |
| Google Sheets | Enquiry tracking integration |

## 📁 Project Structure

```text
midhun_portfolio/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── models.py
│   └── views.py
│
├── static/
│   ├── css/
│   ├── images/
│   └── js/
│
├── templates/
│   ├── base.html
│   └── home.html
│
├── manage.py
├── requirements.txt
└── README.md
```

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/mrbdigitalmarketing2026/midhun-portfolio.git
cd midhun-portfolio
```

### 2. Create a virtual environment

```bash
python -m venv mid
```

### 3. Activate the environment

Windows Command Prompt:

```cmd
mid\Scripts\activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root.

Add your own secure configuration:

```env
SECRET_KEY=your-secure-django-secret-key
DEBUG=True
GOOGLE_SHEETS_WEBHOOK_URL=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

Never upload your `.env` file or expose private credentials.

### 6. Run database migrations

```bash
python manage.py migrate
```

### 7. Create an admin account

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open:

- Website: http://127.0.0.1:8000/
- Admin Dashboard: http://127.0.0.1:8000/admin/

## 📸 Portfolio Projects

Selected work includes projects involving:

- Magic Touch Beauty Salon
- La Belle Salon & Bridal Studio
- MRB Digital Marketing & Advertising

## 📬 Contact

**Midhun Balachandran**

Founder & Managing Director — MRB Digital Marketing & Advertising

- Location: Palakkad, Kerala, India
- Phone: +91 9074492032
- Email: mrb.info.x@gmail.com

## 🔗 Repository

[GitHub — Midhun Portfolio](https://github.com/mrbdigitalmarketing2026/midhun-portfolio)

---

**Built with Python, Django and creativity.**

© Midhun Balachandran. All rights reserved.
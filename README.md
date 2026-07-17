# 📋 Django Task Manager

[![Django CI](https://github.com/mohammad-hussein-dev/django-task-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/mohammad-hussein-dev/django-task-manager/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/mohammad-hussein-dev/django-task-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/mohammad-hussein-dev/django-task-manager)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-6.0%2B-green)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/mohammad-hussein-dev/django-task-manager)](https://github.com/mohammad-hussein-dev/django-task-manager/commits/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

> **A production-ready task management system built with Django** — featuring authentication, task organization, REST API, JWT security, automated testing, Docker support, and cloud deployment.

---

# 📑 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Production Architecture](#-production-architecture)
- [Installation & Usage](#-installation--usage)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Development Workflow](#-development-workflow)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

# 📖 Overview

**Django Task Manager** is a full-featured production-ready task management web application built with Django.

The project provides a modern productivity platform where users can:

- Create and manage tasks
- Organize tasks using categories
- Track deadlines
- Filter and search tasks
- Manage user accounts
- Access REST API endpoints
- Authenticate using JWT tokens

The interface provides visual deadline indicators:

- 🔴 Overdue tasks
- 🟡 Tasks approaching deadline
- 🟢 Future tasks

This project was designed as both a real-world application and a professional Django portfolio project.

---

# 🚀 Live Demo

Production deployment:

🌐 https://django-tasks-mh.up.railway.app

Hosted with:

- Railway
- Gunicorn
- WhiteNoise
- Django production configuration

---

# ✨ Features

| Feature | Description |
|---|---|
| 🔐 Authentication | Complete registration, login, logout system using Django authentication |
| 📝 Task Management | Full CRUD operations for tasks |
| 🏷️ Categories | User-specific task categories |
| ⏰ Deadline Tracking | Smart deadline status indicators |
| 🔍 Search & Filtering | Search tasks and filter by status, priority, category and dates |
| 📊 Dashboard Statistics | Task overview and productivity statistics |
| 🌍 Internationalization | English and Persian language support |
| 📱 Responsive UI | Bootstrap 5 responsive interface |
| 🔌 REST API | API powered by Django REST Framework |
| 🔑 JWT Authentication | Secure token-based API authentication |
| 📘 Swagger Documentation | OpenAPI API documentation |
| 🧪 100% Test Coverage | Comprehensive automated testing |
| ⚡ CI/CD Pipeline | GitHub Actions automated workflow |
| 🐳 Docker Support | Containerized development and deployment |
| ☁️ Cloud Deployment | Production deployment with Railway |

---

# 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python 3.10+, Django 6.0 |
| API | Django REST Framework, Simple JWT |
| API Documentation | drf-spectacular / OpenAPI |
| Frontend | HTML5, CSS3, Bootstrap 5, Font Awesome |
| Database | SQLite (development), PostgreSQL ready |
| Deployment | Railway, Gunicorn |
| Static Files | WhiteNoise |
| Testing | pytest, pytest-django, pytest-cov |
| CI/CD | GitHub Actions, Codecov |
| Code Quality | Black, Ruff, MyPy, Pre-commit |
| Containerization | Docker, Docker Compose |
| Development OS | Arch Linux |

---

# 🏗️ Production Architecture

```

User
|
v
Railway
|
v
Gunicorn
|
v
Django Application
|
+---- Django Templates
|
+---- Django REST API
|
+---- JWT Authentication
|
+---- SQLite/PostgreSQL Database
|
+---- WhiteNoise Static Files

````

---

# 🚀 Installation & Usage

## Option 1: Docker

```bash
git clone https://github.com/mohammad-hussein-dev/django-task-manager.git

cd django-task-manager

docker-compose up -d

docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser
````

Open:

```
http://localhost:8000
```

---

## Option 2: Manual Setup

Clone repository:

```bash
git clone https://github.com/mohammad-hussein-dev/django-task-manager.git

cd django-task-manager
```

Create virtual environment:

```bash
python -m venv .venv

source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

Run server:

```bash
python manage.py runserver
```

---

# 🔐 Environment Variables

Production settings use environment variables.

Example:

```env
DJANGO_SECRET_KEY=your-secret-key

DJANGO_DEBUG=False

DJANGO_ALLOWED_HOSTS=your-domain.com

DATABASE_URL=postgresql://user:password@host/database
```

---

# 📘 API Documentation

The project includes REST API support.

Technologies:

* Django REST Framework
* Simple JWT
* drf-spectacular

Available documentation:

```
/api/schema/
/api/docs/
```

Authentication:

```
JWT Access Token
JWT Refresh Token
```

---

# 🧪 Testing

The project uses pytest.

Current coverage:

```
100%
```

Run tests:

```bash
pytest
```

Coverage report:

```bash
pytest \
--cov=accounts \
--cov=tasks \
--cov=task_manager \
--cov-report=html
```

Open:

```
htmlcov/index.html
```

---

# 📁 Project Structure

```
django-task-manager/

├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py

├── tasks/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── admin.py
│   └── tests.py

├── api/
│   ├── serializers.py
│   ├── views.py
│   └── urls.py

├── task_manager/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py

├── templates/

├── static/

├── tests/

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── pyproject.toml

└── README.md
```

---

# 🛠️ Development Workflow

## Branch Strategy

| Branch    | Purpose            |
| --------- | ------------------ |
| main      | Production branch  |
| develop   | Integration branch |
| feature/* | New features       |
| fix/*     | Bug fixes          |
| hotfix/*  | Emergency fixes    |

---

## Commit Convention

Following Conventional Commits:

```bash
feat(tasks): add filtering system

fix(api): resolve authentication issue

refactor(settings): improve production config

docs(readme): update documentation

test(tasks): add coverage tests
```

---

# Code Quality Tools

| Tool       | Purpose          |
| ---------- | ---------------- |
| Black      | Code formatting  |
| Ruff       | Linting          |
| MyPy       | Type checking    |
| Pre-commit | Automated checks |

Install:

```bash
pre-commit install
```

Run:

```bash
pre-commit run --all-files
```

---

# 🤝 Contributing

Contributions are welcome.

Steps:

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push branch
5. Open Pull Request

Before submitting:

* ✅ Tests pass
* ✅ Code formatted
* ✅ Lint passes
* ✅ Documentation updated

---

# 📄 License

Distributed under the MIT License.

See:

```
LICENSE
```

---

# 👨‍💻 Author

**Mohammad Hussein**

GitHub:

[https://github.com/mohammad-hussein-dev](https://github.com/mohammad-hussein-dev)

Telegram:

[https://t.me/mohammad_hussein_dev](https://t.me/mohammad_hussein_dev)

Email:

[king.mohamd.09876@gmail.com](mailto:king.mohamd.09876@gmail.com)

> "I don't just write code — I simulate the universe."

---

# ⭐ Support the Project

If you find this project useful, consider giving it a star ⭐

It helps others discover the project.

---

Built with 🐧💻 in Arch Linux

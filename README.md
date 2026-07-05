# 📋 Django Task Manager

[![Django CI](https://github.com/mohammad-hussein-dev/django-task-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/mohammad-hussein-dev/django-task-manager/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/mohammad-hussein-dev/django-task-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/mohammad-hussein-dev/django-task-manager)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django-5.1%2B-green)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/mohammad-hussein-dev/django-task-manager)](https://github.com/mohammad-hussein-dev/django-task-manager/commits/main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

> **A professional task management system built with Django** — featuring user authentication, category management, and deadline tracking with visual status indicators.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation & Usage](#-installation--usage)
- [Screenshots](#-screenshots)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Development Workflow](#-development-workflow)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 📖 Overview

**Django Task Manager** is a full-featured, production-ready task management web application built with Django. It provides an intuitive interface for users to **register**, **login**, **create**, **edit**, **delete**, and **categorize** tasks with due dates.

The UI provides clear visual feedback for task urgency using color-coded status indicators — **overdue** (🔴), **soon** (🟡), and **far** (🟢) — making it easy to prioritize work at a glance.

**Perfect for:**
- Personal productivity & daily task tracking
- Team collaboration & project management
- Learning Django best practices & clean architecture
- Portfolio showcase for aspiring Django developers

---

## ✨ Features

| Feature | Description |
| :--- | :--- |
| 🔐 **User Authentication** | Full registration, login, logout using Django's built-in auth system |
| 📝 **Task Management** | Complete CRUD (Create, Read, Update, Delete) operations |
| 🏷️ **Categories** | Organize tasks with user-specific, color‑coded categories |
| ⏰ **Deadline Tracking** | Visual indicators for overdue (🔴), soon (🟡), and far (🟢) deadlines |
| 🌍 **Bilingual Support** | Full support for both **Persian (فارسی)** and **English** |
| 📱 **Responsive UI** | Clean, modern interface built with **Bootstrap 5** |
| 🧪 **100% Test Coverage** | Comprehensive unit tests with `pytest` and `pytest-cov` |
| ⚡ **Production‑Ready** | CI/CD with GitHub Actions, pre‑commit hooks, and Codecov reporting |

---

## 🛠️ Technology Stack

| Category | Technologies |
| :--- | :--- |
| **Backend** | Python 3.10+, Django 5.1+, django-crispy-forms |
| **Frontend** | Bootstrap 5, HTML5, CSS3, Font Awesome |
| **Database** | SQLite (development), PostgreSQL (production-ready) |
| **Testing** | pytest, pytest-django, pytest-cov, coverage.py |
| **CI/CD** | GitHub Actions, Codecov |
| **Code Quality** | Black, Ruff, MyPy, Pre-commit |
| **Containerization** | Docker, Docker Compose |
| **OS** | Arch Linux (development), Any Linux / macOS / Windows (runtime) |

---

## 🚀 Installation & Usage

### Option 1: Using Docker (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/mohammad-hussein-dev/django-task-manager.git
cd django-task-manager

# 2. Start the containers
docker-compose up -d

# 3. Run database migrations
docker-compose exec web python manage.py migrate

# 4. (Optional) Create a superuser
docker-compose exec web python manage.py createsuperuser

# 5. Access the application
open http://localhost:8000
```

### Option 2: Manual Setup (Local)

```bash
# 1. Clone the repository
git clone https://github.com/mohammad-hussein-dev/django-task-manager.git
cd django-task-manager

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -e .[dev]

# 4. Run database migrations
python manage.py migrate

# 5. (Optional) Create a superuser
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver

# 7. Access the application
open http://127.0.0.1:8000
```

---

## 📊 Screenshots

### Task List (English)

| Status | Title | Due Date | Category |
| :---: | :--- | :--- | :--- |
| 🔴 | Buy groceries | Today | Home |
| 🟡 | Finish report | Tomorrow | Work |
| 🟢 | Plan vacation | Next Month | Personal |

*Color coding: 🔴 Overdue · 🟡 Soon (within 3 days) · 🟢 Far (>3 days)*

---

### صفحه‌ی لیست وظایف (فارسی)

| وضعیت | عنوان | مهلت | دسته |
| :---: | :--- | :--- | :--- |
| 🔴 | خرید مواد غذایی | امروز | خانه |
| 🟡 | تکمیل گزارش | فردا | کار |
| 🟢 | برنامه‌ریزی سفر | ماه آینده | شخصی |

---

## 🧪 Testing

The project uses **pytest** with **100% test coverage**.

### Run all tests

```bash
pytest
```

### Run tests with coverage report

```bash
pytest --cov=accounts --cov=tasks --cov=task_manager --cov-report=term --cov-report=html
```

Open `htmlcov/index.html` in your browser for detailed coverage breakdown.

### Test coverage badge

[![codecov](https://codecov.io/gh/mohammad-hussein-dev/django-task-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/mohammad-hussein-dev/django-task-manager)

---

## 📁 Project Structure

```
django-task-manager/
├── accounts/                      # User authentication app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── tasks/                         # Task management app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── task_manager/                  # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   └── css/
│       └── style.css
├── templates/                     # Global templates
│   ├── base.html
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   └── tasks/
│       ├── task_list.html
│       ├── task_detail.html
│       ├── task_form.html
│       └── task_confirm_delete.html
├── tests/                         # Additional test files
│   ├── __init__.py
│   ├── test_admin_*.py
│   ├── test_forms_*.py
│   ├── test_models_*.py
│   └── test_views_*.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── .coveragerc
├── .pre-commit-config.yaml
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── manage.py
├── pyproject.toml
└── README.md
```

---

## 🛠️ Development Workflow

### Branching Strategy

| Branch | Purpose |
| :--- | :--- |
| `main` | Production-ready code |
| `develop` | Integration branch |
| `feature/*` | New features |
| `fix/*` | Bug fixes |
| `hotfix/*` | Critical production fixes |

### Commit Convention

Following [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat(tasks): add deadline filtering
fix(templates): resolve nested with block
refactor(views): simplify queryset
docs(readme): update installation guide
style(css): improve responsive layout
test(forms): add validation tests
chore(deps): update Django to 5.1.3
```

### Code Quality Tools

| Tool | Purpose |
| :--- | :--- |
| **Black** | Code formatting |
| **Ruff** | Linting & import sorting |
| **MyPy** | Static type checking |
| **Pre-commit** | Automated checks before commits |

**Setup pre-commit:**
```bash
pre-commit install
pre-commit run --all-files
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'feat: add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request** against the `develop` branch

**Before submitting a PR, ensure:**
- ✅ All tests pass (`pytest`)
- ✅ Code is formatted (`black .`)
- ✅ Linting passes (`ruff check .`)
- ✅ No commented-out code or debug prints
- ✅ New features include tests
- ✅ Documentation is updated

---

## 📄 License

Distributed under the **MIT License**. See the [LICENSE](LICENSE) file for more information.

---

## 👨‍💻 Author

**Mohammad Hussein**  
- 🌐 GitHub: [@mohammad-hussein-dev](https://github.com/mohammad-hussein-dev)  
- 📧 Email: [king.mohamd.09876@gmail.com](mailto:king.mohamd.09876@gmail.com)  
- 💬 Telegram: [@mohammad_hussein_dev](https://t.me/mohammad_hussein_dev)

> *"I don't just write code — I simulate the universe."*

---

## ⭐ Support the Project

If you found this project helpful, please consider giving it a **star** on GitHub! ⭐  
It helps others discover it and motivates further development.

---

**Built with ❤️ in Arch Linux**
```

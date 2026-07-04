# 📋 Django Task Manager

[![Django CI](https://github.com/mohammad-hussein-dev/django-task-manager/actions/workflows/ci.yml/badge.svg)](https://github.com/mohammad-hussein-dev/django-task-manager/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/mohammad-hussein-dev/django-task-manager/branch/main/graph/badge.svg)](https://codecov.io/gh/mohammad-hussein-dev/django-task-manager)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1%2B-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

> A professional task management system built with Django — featuring user authentication, category management, and deadline tracking with visual status indicators.

---

## 📖 Overview

This project is a full-featured task manager web application built with Django. It allows users to **register**, **login**, **create**, **edit**, **delete**, and **categorize** tasks with due dates. The UI provides clear visual feedback for task urgency using color-coded status indicators (overdue, soon, far).

Perfect for personal productivity, team collaboration, or as a learning resource for Django best practices.

### ✨ Features

- 🔐 **User Authentication** — Register, login, logout with Django's built-in auth system
- 📝 **Task Management** — Full CRUD (Create, Read, Update, Delete) for tasks
- 🏷️ **Categories** — Organize tasks with customizable, color-coded categories
- ⏰ **Deadline Tracking** — Visual indicators for overdue (red), soon (yellow), and far (green) deadlines
- 🌍 **Bilingual** — Full support for both Persian (فارسی) and English
- 📱 **Responsive UI** — Clean, modern interface built with Bootstrap 5
- 🧪 **96% Test Coverage** — Comprehensive unit tests with `pytest` and `pytest-cov`
- ⚡ **Production-Ready** — CI/CD with GitHub Actions, pre-commit hooks, and code coverage reporting

---

## 🧮 Architecture & Design

The project follows Django's **MVT (Model-View-Template)** pattern with a clean separation of concerns:

| Component | Description |
| :--- | :--- |
| **Models** | `Task`, `Category` with relationships, timestamps, and status methods |
| **Views** | Class-based views (`ListView`, `CreateView`, `UpdateView`, `DeleteView`) with mixins |
| **Forms** | `TaskForm`, `CategoryForm` with `crispy-forms` for Bootstrap 5 styling |
| **Templates** | Modular `base.html` with template inheritance and include tags |
| **URLs** | Clean URL routing with app-level `urls.py` and project-level includes |

---

## 🛠️ Installation & Usage

### 1. Clone the repository

```bash
git clone https://github.com/mohammad-hussein-dev/django-task-manager.git
cd django-task-manager
```

### 2. Set up a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install the package with development dependencies

```bash
pip install -e .[dev]
```

### 4. Set up the database

```bash
cd src
python manage.py migrate
```

### 5. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Now open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 📊 Sample Output

### Task List (English)

```
📋 My Tasks
┌────────────────────────────────────────────────────────────┐
│ 🔴 Buy groceries          Due: Today        Category: Home │
│ 🟡 Finish report          Due: Tomorrow     Category: Work │
│ 🟢 Plan vacation          Due: Next Month   Category: Personal │
└────────────────────────────────────────────────────────────┘
```
*Color coding: 🔴 Overdue · 🟡 Soon (within 3 days) · 🟢 Far (>3 days)*

---

### صفحه‌ی لیست وظایف (فارسی)

```
📋 وظایف من
┌────────────────────────────────────────────────────────────┐
│ 🔴 خرید مواد غذایی        مهلت: امروز     دسته: خانه      │
│ 🟡 تکمیل گزارش            مهلت: فردا      دسته: کار       │
│ 🟢 برنامه‌ریزی سفر         مهلت: ماه آینده دسته: شخصی     │
└────────────────────────────────────────────────────────────┘
```

---

## 🧪 Testing

This project uses `pytest` and `pytest-django` for unit testing with **96% test coverage**.

Run the tests:

```bash
cd src
pytest
```

Run tests with coverage report:

```bash
pytest --cov=apps --cov-report=term --cov-report=html
```

Coverage report will be generated in `htmlcov/index.html`. Open it in your browser to see detailed coverage breakdown.

---

## 📁 Project Structure

```
django-task-manager/
├── apps/
│   ├── accounts/                     # User authentication app
│   │   ├── models.py
│   │   ├── views.py                  # LoginView, RegisterView
│   │   ├── urls.py
│   │   ├── tests.py
│   │   └── migrations/
│   └── tasks/                        # Task management app
│       ├── models.py                 # Task, Category models
│       ├── views.py                  # Task CRUD views (CBVs)
│       ├── forms.py                  # TaskForm, CategoryForm
│       ├── urls.py
│       ├── tests.py                  # 32 unit tests
│       └── migrations/
├── src/
│   └── task_manager/                 # Django project settings
│       ├── settings.py
│       ├── urls.py                   # Project-level URL routing
│       ├── wsgi.py
│       └── asgi.py
├── static/
│   └── css/
│       └── style.css                 # Custom styles (Bootstrap 5 + extensions)
├── templates/                        # Django templates
│   ├── base.html                     # Base template with navbar & footer
│   ├── accounts/
│   │   ├── login.html
│   │   └── register.html
│   └── tasks/
│       ├── task_list.html            # Main dashboard
│       ├── task_detail.html
│       ├── task_form.html            # Create/Edit
│       └── task_confirm_delete.html
├── pyproject.toml                    # Project metadata, dependencies, and tool configs
├── .pre-commit-config.yaml           # Pre-commit hooks (ruff, black, etc.)
├── .github/workflows/ci.yml          # GitHub Actions CI
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements, feel free to open an issue or submit a pull request.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Mohammad Hussein** — [GitHub](https://github.com/mohammad-hussein-dev)

---

⭐ If you found this project helpful, consider giving it a star on GitHub!
```

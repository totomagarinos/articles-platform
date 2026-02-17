# AGENTS.md

This document provides guidelines for AI agents and developers working on the **Editorial** project.
Adhere to these conventions to maintain code consistency and quality.

## 1. Environment & Build

The project uses a standard Django setup with a virtual environment (`venv`).

### setup
Ensure the virtual environment is active or use the direct path to the python executable.

```bash
# Activate virtual environment
source venv/bin/activate
# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt
```

### Run Server
```bash
venv/bin/python manage.py runserver
```

### Run Tests
**Run all tests:**
```bash
venv/bin/python manage.py test
```

**Run tests for a specific app:**
```bash
venv/bin/python manage.py test blog
```

**Run a single test case:**
```bash
venv/bin/python manage.py test blog.tests.ArticleTests
```

**Run a specific test method:**
```bash
venv/bin/python manage.py test blog.tests.ArticleTests.test_article_creation
```

### Linting & formatting
No explicit linter configuration file exists. However, follow these rules strictly:
- **Indentation:** **Use 2 spaces** for indentation (Python standard is 4, but this project uses 2).
- **Line Length:** Aim for 79-88 characters, but soft limit 100.
- **Imports:** Sort imports: standard library, Django, third-party, local apps.
- **Quotes:** Use single quotes `'` for strings where possible. Double quotes `"` for docstrings or when containing single quotes.

## 2. Code Style Guidelines

### General
- **Framework:** Django 6.0.
- **Python Version:** 3.x (Compatible with Django 6.0).
- **Project Structure:**
    - `config/`: Project settings and configuration.
    - `users/`: Custom user model and authentication.
    - `blog/`: Blog functionality (Articles, Comments).
    - `templates/`: HTML templates.
    - `static/`: Static assets (CSS, JS).
    - `media/`: User-uploaded content.

### Naming Conventions
- **Variables/Functions:** `snake_case` (e.g., `get_queryset`, `article_list`).
- **Classes:** `PascalCase` (e.g., `ArticleListView`, `CustomUser`).
- **Constants:** `UPPER_CASE` (e.g., `ROLE_CHOICES`, `PUBLISHED`).
- **Files:** `snake_case.py`.

### Models & Database
- **User Model:** Always use `users.CustomUser` or `get_user_model()`. Do not use `django.contrib.auth.models.User` directly.
- **Roles:** Use the defined constants in `CustomUser`:
    - `CustomUser.ADMIN` ("admin")
    - `CustomUser.EDITOR` ("editor")
    - `CustomUser.WRITER` ("writer")
- **Fields:** Define `null=True, blank=True` for optional fields unless logic dictates otherwise.
- **String Representation:** Always implement `__str__` for models.

### Views & URLs
- **Views:** Prefer Class-Based Views (CBVs) over Function-Based Views (FBVs).
    - Use `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`.
    - Mixins: Use `LoginRequiredMixin`, `UserPassesTestMixin` for access control.
- **URLs:** Use `path()` with named routes (e.g., `name='article_detail'`).
- **Reverse:** Use `reverse()` or `reverse_lazy()` for URL resolution.

### Templates
- **Location:** `templates/` directory in root or app-specific `templates/app_name/` directories.
- **Inheritance:** Extend `base.html` (if available) or a common layout.
- **Tags:** Use standard Django template tags (`{% block content %}`, `{% url %}`).

### Error Handling
- Use standard Python `try-except` blocks.
- raise `Http404` or use `get_object_or_404` where appropriate.
- Log errors using Python's `logging` module if needed, rather than `print`.

## 3. Workflow for Agents
1.  **Analyze:** Read relevant files first. Check existing implementations in `views.py` or `models.py` to match style.
2.  **Plan:** Outline changes. Identify if migrations are needed (`makemigrations`).
3.  **Implement:** specific changes. **Respect the 2-space indentation.**
4.  **Verify:** Run tests (`venv/bin/python manage.py test`). Fix any regressions.
5.  **Clean:** Remove unused imports or debug prints.

## 4. Cursor / Copilot Rules
*No specific .cursorrules or .github/copilot-instructions.md found.*
Follow the standard Django best practices and the 2-space indentation rule defined above.

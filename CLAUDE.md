# Claude Code Development Guide

## Project Information
- **Framework**: Django 5.2.5 Blog Application
- **Primary Language**: Python 3.8+
- **Architecture**: MVT (Model-View-Template)

## Development Commands

### Code Quality
```bash
# Linting and formatting
ruff check .
black .
isort .
mypy .

# Testing
pytest
pytest --cov=. --cov-report=html
```

### Django Commands
```bash
# Run development server
python manage.py runserver

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Pre-commit Hooks
This project uses pre-commit hooks for code quality enforcement:
```bash
pre-commit install
pre-commit run --all-files
```

## PR Creation Guidelines

1. Always work on feature branches (not main)
2. Ensure all tests pass
3. Run linting and type checking
4. Write meaningful commit messages
5. Include comprehensive PR descriptions

## Recent Improvements

- Enhanced PR creation workflow
- Added comprehensive development documentation
- Improved project structure clarity
- Better code quality enforcement
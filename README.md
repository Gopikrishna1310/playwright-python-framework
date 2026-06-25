# FieldMountain Automation Framework

A scalable and maintainable UI Automation Framework built using **Playwright**, **Python**, and **Pytest** following the **Page Object Model (POM)** design pattern.

---

## Features

- Playwright (Sync API)
- Python 3.14
- Pytest
- Page Object Model (POM)
- Shared Base Page
- Smart Waits (No Hard Waits)
- HTML Test Reports
- Screenshot Support
- Modular Test Structure
- GitHub Version Control

---

# Project Structure

```
project
│
├── config
├── pages
│   ├── admin
│   ├── annotator
│   ├── aws
│   ├── common
│   ├── datasets
│   ├── files
│   ├── integrations
│   ├── projects
│   ├── restrictions
│   ├── reviewer
│   ├── templates
│   ├── users
│   └── workflows
│
├── tests
│
├── test_data
│
├── utils
│
├── reports
│
├── screenshots
│
├── pytest.ini
├── conftest.py
└── requirements.txt
```

---

# Technologies Used

- Python
- Playwright
- Pytest
- HTML Reports
- Git
- GitHub

---

# Framework Design

- Page Object Model (POM)
- Reusable Base Page
- Smart Wait Utilities
- Modular Test Cases
- Centralized Configuration
- Reusable Components

---

# Test Execution

Run all tests

```bash
pytest
```

Run a specific test

```bash
pytest tests/smoke/test_login.py -v
```

Run with console logs

```bash
pytest tests/smoke/test_login.py -v -s
```

Generate HTML Report

```bash
pytest --html=reports/report.html
```

---

# Reports

After execution

```
reports/
    report.html
```

Open the HTML report in your browser.

---

# Supported Modules

- Login
- Logout
- Users
- Templates
- Projects
- Datasets
- Files
- Restrictions
- Reviewer
- Annotator
- Integrations
- AWS S3 Integration
- Workflows

---

# Best Practices

- No hard waits (`wait_for_timeout()`)
- Smart Playwright waits
- Reusable page methods
- Maintainable architecture
- Clean code structure

---

# Author

**Gopikrishna D**

QA Automation Engineer

Python • Playwright • Pytest
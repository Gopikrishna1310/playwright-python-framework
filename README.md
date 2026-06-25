# FieldMountain Automation Framework

A scalable and maintainable UI Automation Framework built using **Playwright**, **Python**, and **Pytest** following the **Page Object Model (POM)** design pattern.

---

## Features

- Playwright (Sync API)
- Python 3.14
- Pytest 9.0.3
- Page Object Model (POM)
- Shared Base Page with safe helpers (`safe_click`, `safe_fill`, `safe_check`)
- SmartWait utility — zero hard waits (`wait_for_timeout`)
- Condition-based waits throughout (`for_visible`, `for_hidden`, `for_url_contains`)
- Assertions at every Then-step across all modules
- Screenshot on failure (auto-saved to `screenshots/`)
- HTML Test Reports
- Modular test structure with pytest markers
- End-to-end regression suite
- GitHub Version Control

---

## Project Structure

```
FieldMountain automation/
│
├── config/
│   ├── credentials.py          # Admin, Annotator, Reviewer credentials
│   ├── test_data.py            # Integration titles, bucket names, role names
│   └── urls.py                 # BASE_URL
│
├── pages/
│   ├── common/
│   │   ├── base_page.py        # BasePage — safe_click, safe_fill, verify_*, SmartWait
│   │   ├── login_page.py       # Login, org/role selection, logout
│   │   └── sidebar_page.py     # Sidebar navigation helpers
│   ├── annotator/
│   │   └── annotator_page.py   # Annotator login, claim, annotate, submit, logout
│   ├── aws/
│   │   ├── aws_login_page.py   # AWS console login
│   │   ├── aws_iam_page.py     # IAM policy edit
│   │   ├── aws_role_page.py    # IAM role creation wizard
│   │   └── aws_s3_page.py      # S3 bucket CORS configuration
│   ├── datasets/
│   │   └── datasets_page.py
│   ├── files/
│   │   └── files_page.py
│   ├── integrations/
│   │   └── s3_integration_page.py
│   ├── projects/
│   │   └── projects_page.py
│   ├── restrictions/
│   │   └── restrictions_page.py
│   ├── reviewer/
│   │   └── reviewer_page.py    # Reviewer login, claim, reject, approve, logout
│   ├── templates/
│   │   └── templates_page.py
│   ├── users/
│   │   └── users_page.py
│   └── workflows/
│       └── workflows_page.py
│
├── tests/
│   ├── smoke/
│   │   └── test_login.py
│   ├── integrations/
│   │   └── test_full_s3_integration_flow.py
│   ├── files/
│   │   └── test_files_actions.py
│   ├── datasets/
│   │   └── test_dataset_actions.py
│   ├── templates/
│   │   └── test_template_actions.py
│   ├── workflows/
│   │   └── test_workflows_actions.py
│   ├── users/
│   │   └── test_users_actions.py
│   ├── projects/
│   │   └── test_projects_actions.py
│   ├── restrictions/
│   │   └── test_restrictions_actions.py
│   ├── annotator/
│   │   └── test_annotator_actions.py
│   ├── reviewer/
│   │   └── test_reviewer_actions.py
│   └── regression/
│       └── test_full_regression.py
│
├── test_data/
│   ├── files/
│   │   ├── audio/              # .mp3, .wav, .aac, .flac files
│   │   └── template/           # .zip template files
│   └── credentials/
│
├── utils/
│   ├── waits.py                # SmartWait — for_visible, for_hidden, for_url_contains
│   └── constants.py            # SHORT=5000, DEFAULT=30000, LONG=60000, LOAD=45000
│
├── reports/
│   └── report.html
│
├── screenshots/                # Auto-saved on test failure
│
├── conftest.py                 # Browser fixture, viewport, screenshot hook
├── pytest.ini                  # Markers, addopts, log config
└── requirements.txt
```

---

## Technologies Used

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14 | Core language |
| Playwright | latest | Browser automation (Sync API) |
| Pytest | 9.0.3 | Test runner and reporting |
| pytest-html | 4.2.0 | HTML report generation |
| pytest-metadata | 3.1.1 | Report metadata |
| Chromium | bundled | Test browser |

---

## Framework Design

### Page Object Model (POM)
Every page has its own class under `pages/`. Tests call page methods — no locators in test files.

### BasePage
All page objects extend `BasePage`, which provides:
- `safe_click()` — auto-waits for visible + enabled before clicking
- `safe_fill()` — clears and fills with auto-wait
- `safe_check()` — checks a checkbox with auto-wait
- `verify_visible()` — asserts element is visible
- `verify_hidden()` — asserts element is hidden
- `verify_enabled()` — asserts element is enabled
- `verify_disabled()` — asserts element is disabled
- `verify_count()` — asserts element count (used for delete verification)
- `verify_url()` — asserts current URL matches pattern
- `read_clipboard()` — reads clipboard content with prefix validation

### SmartWait
`utils/waits.py` provides condition-based waits used everywhere:
- `wait.for_visible(locator)` — waits until element is visible
- `wait.for_hidden(locator)` — waits until element disappears
- `wait.for_url_contains(path)` — waits until URL contains string
- `wait.for_url_not_contains(path)` — waits until URL loses string
- `wait.for_page_ready()` — waits for DOM + network to settle

### Zero Hard Waits
`wait_for_timeout()` is never used for app-readiness. The only two retained `wait_for_timeout` calls are test actions (recording audio for 5 seconds), not waits for UI.

### Assertions at Every Then-Step
Every test scenario's Then-step has its own `verify_*()` call. Assertions are never silent.

---

## Test Execution

### Run all tests
```bash
pytest
```

### Run a specific module
```bash
pytest tests/smoke/test_login.py -v -s
pytest tests/datasets/test_dataset_actions.py -v -s
pytest tests/templates/test_template_actions.py -v -s
pytest tests/workflows/test_workflows_actions.py -v -s
pytest tests/users/test_users_actions.py -v -s
pytest tests/projects/test_projects_actions.py -v -s
pytest tests/restrictions/test_restrictions_actions.py -v -s
```

### Run by marker
```bash
pytest -m smoke -v -s
pytest -m datasets -v -s
pytest -m templates -v -s
pytest -m workflows -v -s
pytest -m users -v -s
pytest -m projects -v -s
pytest -m restrictions -v -s
pytest -m regression -v -s
```

### Run S3 integration (requires AWS credentials)
```bash
pytest tests/integrations/test_full_s3_integration_flow.py -v -s
```

### Run full end-to-end regression
```bash
pytest tests/regression/test_full_regression.py -v -s -m regression
```

### Generate HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Watch mode (slow motion for debugging)
```bash
set SLOW_MO=500   # Windows PowerShell
pytest tests/smoke/test_login.py -v -s
```

---

## Recommended Execution Order

Run modules in this order to satisfy data dependencies:

```
1.  pytest tests/smoke/                    # Login verification
2.  pytest tests/integrations/             # S3 bucket integration setup
3.  pytest tests/files/                    # Upload audio files
4.  pytest tests/datasets/                 # Create datasets and add files
5.  pytest tests/templates/                # Upload templates (.zip)
6.  pytest tests/workflows/                # Create workflows with annotate nodes
7.  pytest tests/users/                    # Create annotator and reviewer users
8.  pytest tests/projects/                 # Create project, assign users and datasets
9.  pytest tests/restrictions/             # Validate protected item deletion is blocked
10. pytest tests/annotator/                # Annotator flow
11. pytest tests/reviewer/                 # Reviewer flow
12. pytest tests/regression/               # Full end-to-end regression
```

---

## Configuration

### Viewport
Fixed at **1536×864** in `conftest.py`. `--start-maximized` is intentionally excluded to ensure consistent layout across different physical screen sizes.

### Timeouts
Defined in `conftest.py` and `utils/waits.py`:

| Constant | Value | Used for |
|---|---|---|
| `SHORT` | 5,000ms | Near-instant operations (redirects, toasts) |
| `DEFAULT` | 30,000ms | Standard element interactions |
| `LONG` | 60,000ms | Backend writes, list updates |
| `LOAD` | 45,000ms | Page navigation |

### Screenshots
Automatically saved to `screenshots/` on any test failure. Filename includes the test name:
```
screenshots/test_template_actions__failure.png
```

---

## Reports

After execution, open the HTML report:
```
reports/report.html
```

---

## Supported Modules

| Module | Marker | Description |
|---|---|---|
| Login | `smoke` | Admin login with org and role selection |
| S3 Integration | `s3` | Full AWS IAM + S3 CORS setup |
| Files | `files` | Upload, validate, delete files |
| Datasets | `datasets` | Create datasets, add/remove files |
| Templates | `templates` | Upload .zip templates, delete |
| Workflows | `workflows` | Create workflow with canvas nodes and edges |
| Users | `users` | Create users, status changes (single and bulk) |
| Projects | `projects` | Create project, assign datasets, users, tasks |
| Restrictions | `restrictions` | Validate deletion blocked for project-linked items |
| Annotator | `annotator` | Claim task, record audio, submit annotation |
| Reviewer | `reviewer` | Claim task, reject, approve |
| Regression | `regression` | Full end-to-end flow across all modules |

---

## Best Practices

- No `wait_for_timeout()` for app-readiness — all waits are condition-based
- Every Then-step has its own `verify_*()` assertion
- URL verified with `$`-anchored regex to avoid substring matches
- `page.reload()` before delete verification to bypass optimistic DOM
- Dialog-scoped button clicks to avoid toolbar/popup name collisions
- Clipboard reads use `expected_prefix` to catch empty or wrong values
- File format validated before upload (`.zip` assertion for templates)

---

## Author

**Gopikrishna D**

QA Engineer — Python • Playwright • Pytest
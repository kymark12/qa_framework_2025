# 🧪 Marky 2025 QA Automation Framework

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-8.0.0-green.svg)](https://docs.pytest.org/)
[![Playwright](https://img.shields.io/badge/playwright-1.41.0-orange.svg)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Live Dashboard](https://img.shields.io/badge/Dashboard-Live-success.svg)](https://appframework2025-mupyhx5frbro3tvwrmuxaq.streamlit.app/)

A modern, scalable test automation framework demonstrating professional QA engineering practices. This framework showcases expertise in API testing, UI automation, and comprehensive test reporting with CI/CD integration.

> **⚠️ Disclaimer:** This repository is for educational and portfolio demonstration purposes only.
> 
> **Test Applications Used:**
> - **UI Testing**: [SauceDemo](https://www.saucedemo.com/) - An open-source demo application created by Sauce Labs specifically for testing practice
> - **API Testing**: [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - A free fake REST API for testing and prototyping
> 
> Both applications are publicly available and explicitly designed for testing practice and educational purposes.

---

## 📋 Table of Contents

- [Features](#-features)
- [Live Dashboard](#-live-dashboard)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Running Tests](#-running-tests)
- [Test Reports](#-test-reports)
- [CI/CD Integration](#-cicd-integration)
- [Best Practices](#-best-practices)
- [Contact](#-contact)

---

## ✨ Features

- **Multi-Layer Testing**: API, UI (E2E), and Unit tests
- **Modern Tools**: Playwright for UI automation, Pytest for test execution
- **Professional Reporting**: Allure reports with detailed test analytics
- **Live Dashboard**: Real-time test results visualization with Streamlit
- **CI/CD Ready**: GitHub Actions workflow for automated testing
- **Scalable Architecture**: Modular design with fixtures and reusable components
- **Best Practices**: Page Object Model, fixture management, test isolation
- **Type Safety**: Python type hints for better code quality
- **Version Control**: Pinned dependencies for reproducible environments

---

## 🛠 Tech Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.12+ |
| **Test Framework** | Pytest 8.0.0 |
| **UI Automation** | Playwright 1.41.0 |
| **API Testing** | Requests 2.31.0 |
| **Reporting** | Allure 2.13.2 + Streamlit Dashboard |
| **Dashboard** | Streamlit 1.31.0 |
| **CI/CD** | GitHub Actions |
| **Package Management** | virtualenv |

---

## 📁 Project Structure
```
marky_2025_qa_framework/
├── .github/
│   └── workflows/          # CI/CD pipeline configurations
│       ├── ci.yml          # Main test execution workflow
│       └── cleanup-reports.yml
├── .streamlit/             # Streamlit configuration
├── docs/                   # Documentation
├── fixtures/               # Test data and fixtures
├── reports/                # Generated test reports
│   ├── report.json         # Latest test results (JSON)
│   └── allure-results/     # Allure report data
├── src/
│   └── dashboards/
│       └── pytest_streamlit_dashboard.py  # Live dashboard
├── tests/
│   ├── api/                # API test suite
│   │   └── test_api.py 
│   ├── ui/                 # UI/E2E test suite
│   │   └── test_login.py 
│   └── unit/               # Unit test suite
├── conftest.py             # Pytest fixtures and configuration
├── pytest.ini              # Pytest settings
├── requirements.txt        # Dashboard dependencies
├── requirements-dev.txt    # Development/testing dependencies
└── README.md 
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- Git
- Virtual environment tool (virtualenv)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/marky_2025_qa_framework.git
   cd marky_2025_qa_framework
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt

   # For dashboard only
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest
```
### API tests only
```bash
pytest tests/api/
```
### UI tests only
```bash
pytest tests/ui/
```
### Unit tests only
```bash
pytest tests/unit/
```
### Run Tests by Markers
```bash
# E2E tests
pytest -m e2e

# Smoke tests
pytest -m smoke

# Slow tests
pytest -m slow
```

### Run with Verbose 
```bash
pytest -v
```

### Run with Coverage
```bash
pytest --cov=src --cov-report=html
```

---

## 📊 Test Reports

### 1. Live Streamlit Dashboard

**[View Live Dashboard →](https://appframework2025-mupyhx5frbro3tvwrmuxaq.streamlit.app/)**

Automatically updated with every test run via CI/CD pipeline.

### 2. Allure Reports

#### Generate Allure Reports

```bash
# Run tests with Allure
pytest --alluredir=./reports/allure-results

# View the report
allure serve ./reports/allure-results
```

### 3. JSON Report

```bash
# Generate JSON report (automatically created by pytest)
pytest --json-report --json-report-file=./reports/report.json

# View raw JSON
cat reports/report.json
```

The framework automatically generates:
1. ✅ Test execution summaries
2. 📝 Detailed step-by-step logs
3. 📸 Screenshots on failures (UI tests)
4. 🌐 API request/response details
5. 📈 Trend analysis over multiple runs

---

## 🔄 CI/CD Integration

This framework includes **GitHub Actions workflows** for continuous testing:

### Main CI Workflow (`.github/workflows/ci.yml`)

- ✅ Automated test execution on push/PR
- ✅ Playwright browser installation
- ✅ Test execution with retry logic (2 retries)
- ✅ Automatic report generation and archiving
- ✅ Report publishing to `reports` branch
- ✅ Artifact uploads (Allure results, JSON reports, screenshots)

### Report Cleanup Workflow (`.github/workflows/cleanup-reports.yml`)

- 🗑️ Scheduled cleanup of old archived reports (weekly)
- 🔢 Keeps the 20 most recent reports
- 📦 Prevents repository bloat

### Dashboard Auto-Update

The Streamlit dashboard automatically:
1. Fetches the latest `report.json` from the `reports` branch
2. Updates visualizations in real-time
3. Shows current test execution status

---

## 🎯 Best Practices Demonstrated

- **Test Organization**: Clear separation of API, UI, and unit tests
- **Fixture Management**: Reusable fixtures in conftest.py
- **Configuration Management**: Environment-specific configs
- **Page Object Model**: Maintainable UI test structure
- **API Client Pattern**: Centralized API interaction logic
- **Version Pinning**: Reproducible dependency management
- **Documentation**: Comprehensive inline and README docs
- **CI/CD Integration**: Automated testing pipeline
- **Reporting**: Professional test reports with Allure
- **Code Quality**: Clean, readable, and maintainable code
- **Failure Tracking**: Intentional failure scenarios for comprehensive testing

---

## 📚 Key Testing Concepts

### API Testing

- RESTful API endpoint validation
- Request/response verification
- Authentication handling
- Error handling and edge cases

### UI Testing

- End-to-end user workflows
- Cross-browser compatibility
- Page Object Model implementation
- Element interaction strategies

### Test Data Management

- Fixture-based data provisioning
- Environment-specific configurations
- Test isolation and cleanup

## 🤝 Contributing

This is a portfolio project, but feedback and suggestions are welcome! Feel free to:

- Open an issue for discussions
- Fork the repository for your own learning
- Reach out with questions or suggestions

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Contact

Mark Ivan Berbenzana**

- 📧 Email: marky.berbenzana@gmail.com
- 💼 LinkedIn: [Mark Ivan Berbenzana](https://www.linkedin.com/in/mark-ivan-berbenzana-841093bb/)
- 🐙 GitHub: https://github.com/kymark12
- 📊 Live Dashboard: [View Test Results](https://appframework2025-mupyhx5frbro3tvwrmuxaq.streamlit.app/)

---

## 🙏 Acknowledgments

- Pytest team for the excellent testing framework
- Playwright team for modern browser automation
- Allure for beautiful test reporting
- Streamlit for interactive dashboard capabilities
- Open source community for continuous inspiration

---

## 📸 Dashboard Preview

Visit the **[Live Dashboard](https://appframework2025-mupyhx5frbro3tvwrmuxaq.streamlit.app/)** to see:
- Real-time test metrics
- Failure analysis with detailed information
- Performance insights and slowest tests
- Comprehensive test coverage visualization

---

⭐ If you find this project helpful, please consider giving it a star!

**Last Updated**: December 2025
## 💼 For Hiring Managers & Freelance Clients

### What This Demonstrates

**QA Automation Engineering Skills:**
- ✅ Scalable test architecture (Page Objects, API Client patterns)
- ✅ Reliable CI/CD integration (deterministic tests, flaky management, artifact handling)
- ✅ Professional code quality (linting, type hints, pre-commit hooks)
- ✅ Risk-based testing strategy (smoke/regression prioritization, negative cases)
- ✅ Debugging excellence (logging, tracing, actionable failure messages)

**How I Adapt This for Your Needs:**
- Swap config → your app's auth/environments
- Add your API endpoints → reuse client pattern
- Adapt UI pages → your design patterns
- Plug into your CI → GitHub Actions/Jenkins/GitLab/Azure
- **Typical engagement:** smoke suite (5–7 days) → regression pack (2–3 weeks) → live dashboard

---
# 🧪 Marky 2025 QA Automation Framework

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Pytest](https://img.shields.io/badge/pytest-8.0.0-green.svg)](https://docs.pytest.org/)
[![Playwright](https://img.shields.io/badge/playwright-1.41.0-orange.svg)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
| **Reporting** | Allure 2.13.2 |
| **CI/CD** | GitHub Actions |
| **Package Management** | virtualenv |

---

## 📁 Project Structure
```
marky_2025_qa_framework/
├── .github/
│ └── workflows/ # CI/CD pipeline configurations
│ └── ci.yml
├── docs/ # Documentation and design documents
├── fixtures/ # Test data and fixtures
├── reports/ # Generated test reports
├── src/ # Source code (page objects, utilities)
├── tests/
│ ├── api/ # API test suite
│ ├── ui/ # UI/E2E test suite
│ │ └── test_login.py
│ └── unit/ # Unit test suite
├── conftest.py # Pytest fixtures and configuration
├── pytest.ini # Pytest settings
├── requirements.txt # Project dependencies
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
```
### Run with Verbose 
```bash
pytest -v
```
### Run with Coverage
``` bash
pytest --cov=src --cov-report=html
```

## 📊 Test Reports
### Generate Allure Reports

#### 1. Run tests with Allure
``` bash
   pytest --alluredir=./reports/allure-results
```

#### 2. View the report
``` bash
   allure serve ./reports/allure-results
```

The framework automatically generates:
1. Test execution summaries
2. Detailed step-by-step logs
3. Screenshots on failures (UI tests)
4. API request/response details
5. Trend analysis over multiple runs

## 🔄 CI/CD Integration

This framework includes GitHub Actions workflow for continuous testing:

- ✅ Automated test execution on push/PR
- ✅ Multi-environment testing (staging, production)
- ✅ Automatic report generation and archiving
- ✅ Slack/Email notifications on failures
- ✅ Parallel test execution for faster feedback

Workflow location: `.github/workflows/ci.yml`

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

Mark Ivan Berbenzana

- 📧 Email: marky.berbenzana@gmail.com
- 💼 LinkedIn: [Mark Ivan Berbenzana](https://www.linkedin.com/in/mark-ivan-berbenzana-841093bb/)
- 🐙 GitHub: https://github.com/kymark12

## 🙏 Acknowledgments

- Pytest team for the excellent testing framework
- Playwright team for modern browser automation
- Allure for beautiful test reporting
- Open source community for continuous inspiration

⭐ If you find this project helpful, please consider giving it a star!

Last Updated: November 2025
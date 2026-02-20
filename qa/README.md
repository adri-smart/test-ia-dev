# Conversational Agent - E2E Test Suite

This project contains the End-to-End (E2E) tests for the Conversational Agent application, implemented using [Playwright](https://playwright.dev/).

## 🧪 What is being tested?

This test suite validates the core features of the Conversational Agent from a user's perspective. The main goal is to ensure the application correctly interprets natural language queries, processes them, and returns accurate and useful information.

The tests cover the following key user stories and features:
- **(KAN-469, KAN-470, KAN-471)**: Natural Language Processing (NLP) of user queries.
- **(KAN-472, KAN-473, KAN-474, KAN-475)**: SQL generation, execution, and validation.
- **(KAN-477, KAN-478, KAN-479)**: Conversational flow and state management.
- **(KAN-476, KAN-480, KAN-481, KAN-482, KAN-483, KAN-484)**: Data analysis, segmentation, and insight generation.
- **(KAN-466, KAN-467)**: Secure connection to external services (Gemini, Database).
- And more, covering all 21 user stories provided.

## 📋 Prerequisites

Before running the tests, ensure you have the following installed:
- [Node.js](https://nodejs.org/) (v20.x or later)
- [npm](https://www.npmjs.com/) (comes with Node.js)
- A running instance of the Conversational Agent application.

## 🚀 Getting Started

### 1. Installation

The project dependencies are managed in the `qa/` directory. To install them, run the following command from the **root** of the repository:

```bash
npm install --prefix qa
```

This will install Playwright, all other dependencies from `package.json`, and automatically download the required browser binaries.

### 2. Environment Configuration

The tests require an environment file to know the base URL of the application.

1.  From the root of the repository, create a `.env` file in the `qa/` directory:
    ```bash
    cp qa/.env.example qa/.env
    ```
2.  Open `qa/.env` and modify the `BASE_URL` if your application is running on a different address than the default (`http://localhost:8080`).

### 3. Running the Tests

To execute the entire test suite, run the following command from the **root** of the repository:

```bash
npm test --prefix qa
```
This will run all tests in headless mode across the configured browsers.

To run tests in UI mode for debugging:
```bash
npm test --prefix qa -- --ui
```

### 4. Viewing Test Reports

After a test run is complete, an HTML report is generated. To view it, run:

```bash
npm run report --prefix qa
```
This will open the report in your default web browser.

## 📂 Project Structure

The project follows the Page Object Model (POM) pattern to ensure the code is maintainable, reusable, and easy to understand.

```
qa/
├── .github/workflows/        # CI/CD pipeline for GitHub Actions
│   └── playwright.yml
├── tests/                    # Contains all E2E test files (*.spec.ts)
│   └── query.spec.ts
├── pages/                    # Page Object Model classes
│   ├── base.page.ts
│   └── query.page.ts
├── components/               # Reusable UI components (e.g., Navbar, Modal)
├── fixtures/                 # Test data files (e.g., users.json)
├── helpers/                  # Utility functions and helper classes
├── .env.example              # Example environment variables
├── .gitignore                # Files to be ignored by Git
├── package.json              # Project dependencies and scripts
├── playwright.config.ts      # Main Playwright configuration
├── README.md                 # This file
└── tsconfig.json             # TypeScript compiler options
```

## ✍️ Conventions and Standards

- **Selectors**: Prioritize `data-testid` attributes for locating elements to decouple tests from CSS or JS changes.
- **Page Objects**: All interactions with a page (locating elements, filling forms, clicking buttons) should be encapsulated within its Page Object class.
- **Tests**: Tests should be independent and self-contained. Use `beforeEach` and `afterEach` hooks for setup and teardown. Follow the Arrange-Act-Assert pattern.
- **File Naming**: Test files should end with `.spec.ts`. Page object files should end with `.page.ts`.

## ➕ How to Add New Tests

1.  **Create/Update Page Object**: If testing a new page, create a new file in `pages/` (e.g., `dashboard.page.ts`). If the page already has a Page Object, add new selectors and methods for the elements you need to interact with.
2.  **Create Test File**: Create a new test file in the `tests/` directory (e.g., `dashboard.spec.ts`).
3.  **Write the Test**: Import the necessary Page Objects and write your test using `test()` and `expect()`.
4.  **Run and Verify**: Run your new test to ensure it passes and correctly validates the feature.

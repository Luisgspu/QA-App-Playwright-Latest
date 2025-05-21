# QA-App-Allure-Testing

## Overview
This project is designed for automated testing of web applications using [Playwright](https://playwright.dev/python/), [pytest](https://docs.pytest.org/), and [Allure](https://docs.qameta.io/allure/). It includes modules for handling screenshots, XHR responses, cookies, and API interactions, as well as a suite of test cases that validate different functionalities of the application.

## Project Structure
```
QA-App-Allure-Testing
├── .github
│   ├── workflows
│      ├── main.yml
│      ├── reset-allure-history.yml
│      └── scheduled.yml
├── Utils
│   ├── ScreenshotHandler.py
│   ├── XHRResponseCapturer.py
│   ├── CookiesHandler.py
│   ├── CTAHandlerDOM.py
│   ├── CTAVerifier.py
│   ├── CreateDriver.py
│   ├── CreateAPIandXHR.py
│   ├── VerifyPersonalizationAndCapture.py
│   ├── vehicle_api.py
│   ├── modelcodesAPI.py
│   └── ImageVerifier.py
├── Tests
│   ├── test_bfv1_playwright.py
│   ├── test_bfv2_playwright.py
│   ├── test_bfv3_playwright.py
│   ├── test_LastConfigStarted_playwright.py
│   ├── test_LastConfigCompleted_playwright.py
│   ├── test_LastSeenSRP_playwright.py
│   ├── test_LastSeenPDP_playwright.py
│   ├── PersonalizedCTA1_test_playwright.py
│   ├── PersonalizedCTA2_test_playwright.py
│   ├── PersonalizedCTA3_test_playwright.py
│   └── PersonalizedCTA4_test_playwright.py
├── test_dictionaries
│   ├── BFV1.json
│   ├── BFV2.json
│   ├── BFV3.json
│   ├── Last Seen SRP.json
│   ├── Last Seen PDP.json
│   ├── Last Configuration Started.json
│   └── Las Configuration Completed.json
├── requirements.txt
├── QAAppAllure.py
├── pytest.ini
├── .gitignore
├── Dockerfile
└── README.md
```

## Setup Instructions

1. **Clone the repository**:
   ```sh
   git clone <repository-url>
   cd QA-App-Allure-Testing
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then run:
   ```sh
   pip install -r requirements.txt
   ```

3. **Install Playwright Browsers**:
   After installing Playwright, you need to install the necessary browsers:
   ```sh
   playwright install
   ```

## Test Flow

The main test orchestration is handled in `QAAppAllure.py`. Here’s how the test flow works:

1. **Defining Test Cases**  
   - The `manual_test_cases` list in `QAAppAllure.py` defines which tests to run.
   - Each entry specifies a `test_name`, `market_code`, and optionally a `model_code`.
     - If `model_code` is provided: Only that specific model will be tested for the given market and test type.
     - If `model_code` is omitted or set to `None`: The test will run for **all available models** in the specified market for that test type.

2. **Fetching URLs and Building Test Cases**  
   - For each entry in `manual_test_cases`, the script calls the `VehicleAPI` to fetch all necessary URLs and metadata for the test.
     - If a `model_code` is specified, only URLs for that model are fetched.
     - If no `model_code` is specified, the API returns URLs for **all models** in that market, and a test case is created for each model.
   - The result is a combined list of test cases (`all_test_cases`) that includes both manually specified and dynamically generated cases.

3. **Test Execution**  
   - The test runner uses `pytest.mark.parametrize` to execute the `test_run` function for each test case in `all_test_cases`.
   - For each test case:
     1. The test context is set up (browser, context, page, XHR capturer, etc.).
     2. The appropriate test logic is selected based on `test_name` (e.g., BFV1, Last Configuration Started, etc.).
     3. The test navigates to the required URLs, performs actions, and validates personalization/campaign logic.
     4. Results and failures are reported to Allure.

4. **Allure Reporting**  
   - Each test case is reported in Allure with details such as market, model, test type, and any relevant tags.
   - If you specify a `model_code` in `manual_test_cases`, only that model is tested and reported.
   - If you omit `model_code`, **all models** for the given market and test type are tested and reported as separate suites in Allure.

### Example

```python
manual_test_cases = [
    {"test_name": "BFV1", "market_code": "DE/de", "model_code": "S214"},  # Only S214 model
    {"test_name": "Last Seen SRP", "market_code": "DE/de"},               # All models in DE/de
]
```
- The first entry will test only the S214 model for BFV1 in DE/de.
- The second entry will test **all models** for "Last Seen SRP" in DE/de.

## Running Tests

To run all tests in parallel with reruns and Allure reporting, use the following command:

```sh
pytest QAAppAllure.py -n 4 -s -v --reruns 4 --alluredir=allure-results
```

- `-n 4` runs tests in parallel using 4 CPU cores. Adjust this number based on your machine's available cores.
- `--reruns 4` will rerun any failed test up to 4 times.
- `--alluredir=allure-results` saves the results for Allure reporting.
- `-s` allows print/log output to be shown in the console.
- `-v` enables verbose output.

You can change the values for `-n` and `--reruns` depending on your hardware and reliability needs.

---

## Allure Reporting

After running your tests, you can generate and view the Allure report locally with the following commands (for example, if Allure is installed at `C:\Allure\allure-2.33.0\bin`):

```sh
C:\Allure\allure-2.33.0\bin\allure generate allure-results -o allure-report --clean
C:\Allure\allure-2.33.0\bin\allure serve allure-results
```

- The first command generates a static HTML report in the `allure-report` folder.
- The second command starts a local server to view the report in your browser.

Make sure to adjust the path if your Allure installation is in a different location.

## Running Tests with Docker

You can also run your tests in a fully isolated and reproducible environment using Docker. This is especially useful for CI/CD pipelines and when deploying to cloud environments like Azure Kubernetes Service.

### 1. Build the Docker image

```sh
docker build -t qa-app-allure .
```

### 2. Run the tests in a Docker container

```sh
docker run --rm -v "${PWD}\allure-results:/app/allure-results" qa-app-allure
```
> On Linux/macOS, use `-v "$PWD/allure-results:/app/allure-results"` instead.

This command will execute your tests inside the container and save the Allure results to your local `allure-results` directory.

### 3. Generate and view the Allure report

After running the tests, generate and serve the Allure report as usual:

```sh
C:\Allure\allure-2.33.0\bin\allure generate allure-results -o allure-report --clean
C:\Allure\allure-2.33.0\bin\allure serve allure-results
```

### Dockerfile Example

Your project includes a `Dockerfile` similar to the following:

```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install playwright && playwright install --with-deps

COPY . .

CMD ["pytest", "QAAppAllure.py", "-n", "4", "-s", "-v", "--reruns", "4", "--alluredir=allure-results"]
```

This ensures your tests run in a consistent environment, both locally and in CI/CD.

## .gitignore

A recommended `.gitignore` for this project:

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
.eggs/
*.log

# VSCode
.vscode/
.history/

# Tests
/Tests/*.png


# Allure
allure-results/
allure-report/

# Pytest
.cache/
.pytest_cache/

# OS
.DS_Store
Thumbs.db
ehthumbs.db
desktop.ini

# Environment
.env
.env.*
.venv/
venv/
ENV/
env/
pip-log.txt

# Misc
*.swp
*.bak
*.tmp
*.orig

# Jupyter
.ipynb_checkpoints/

# Coverage
htmlcov/
.coverage
.tox/
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover

# MyPy
.mypy_cache/
.dmypy.json
.pyre/
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
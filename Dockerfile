FROM python:3.11

# Set work directory
WORKDIR /app

# Install system dependencies (if needed)
# RUN apt-get update && apt-get install -y <other-deps>

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN pip install playwright && playwright install --with-deps

# Copy the rest of your code
COPY . .

# Default command (can be overridden)
CMD ["pytest", "QAAppAllure.py", "-n", "4", "-s", "-v", "--reruns", "4", "--alluredir=allure-results"]
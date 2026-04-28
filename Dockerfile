FROM python:3.12-slim

# Set working directory
WORKDIR /app

# 1. Copy requirements from the outer folder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the entire project content
COPY . .

# 3. Tell Docker to run manage.py from the 'core' subfolder
# Note the path: core/manage.py
CMD ["python", "core/manage.py", "runserver", "0.0.0.0:8000"]
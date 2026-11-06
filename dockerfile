# 1. Use Python 3.12 as the base image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy dependency list into the container
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code into the container
COPY app.py .

# 6. Document the application port
EXPOSE 5000

# 7. Set default application port
ENV PORT=5000

# 8. Start the Flask application
CMD ["python", "app.py"]

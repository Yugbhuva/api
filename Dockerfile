FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Create logs folder (if needed)
RUN mkdir -p logs

# Expose port for Render (default FastAPI port)
EXPOSE 8000

# Start via Python runner in main.py (uses settings)
CMD ["python", "-m", "app.main"]

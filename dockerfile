# -------------------------------
# 1. Use Python Base Image
# -------------------------------
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# -------------------------------
# 2. Install System Dependencies
# -------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------
# 3. Copy project files
# -------------------------------
    
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create directories inside container
RUN mkdir -p /app/faiss_indexes
RUN mkdir -p /app/logs

# -------------------------------
# 4. Expose FastAPI port
# -------------------------------
EXPOSE 8000

# -------------------------------
# 5. Run the FastAPI app
# -------------------------------
CMD ["python", "-m", "src.main"]
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir mitmproxy

# Copy application files
COPY . .

# Expose default mitmproxy port
EXPOSE 8080

# Default command
ENTRYPOINT ["mitmdump"]
CMD ["-s", "mitm_false2true.py", "--listen-host", "0.0.0.0"]

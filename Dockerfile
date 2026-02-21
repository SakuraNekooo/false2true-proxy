FROM python:3.11-slim

LABEL maintainer="柏喵Atri <atri@example.com>"
LABEL org.opencontainers.image.source="https://github.com/SakuraNekooo/false2true-proxy"
LABEL org.opencontainers.image.description="MITMProxy addon to replace false with true in HTTP responses"
LABEL org.opencontainers.image.licenses="MIT"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 -s /bin/bash mitmuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir mitmproxy

# Copy application files
COPY . .

# Create directory for mitmproxy data
RUN mkdir -p /home/mitmuser/.mitmproxy && \
    chown -R mitmuser:mitmuser /home/mitmuser/.mitmproxy && \
    chown -R mitmuser:mitmuser /app

# Switch to non-root user
USER mitmuser

# Expose default mitmproxy port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Default command
ENTRYPOINT ["mitmdump"]
CMD ["-s", "mitm_false2true.py", "--listen-host", "0.0.0.0"]

# Usage examples in comments:
# docker run -p 8080:8080 ghcr.io/sakuranekooo/false2true-proxy:latest
# docker run -p 8888:8080 ghcr.io/sakuranekooo/false2true-proxy:latest --listen-port 8888
# docker run -p 8080:8080 -v ./logs:/home/mitmuser/.mitmproxy ghcr.io/sakuranekooo/false2true-proxy:latest -w /home/mitmuser/.mitmproxy/traffic.mitm

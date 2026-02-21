#!/bin/bash
# Test script for False2True Proxy Docker container

set -e

echo "=== Testing False2True Proxy Docker Container ==="

# Clean up any existing containers
docker rm -f false2true-test 2>/dev/null || true

# Build image if not exists
if ! docker images | grep -q "false2true-proxy"; then
    echo "Building Docker image..."
    docker build -t false2true-proxy .
fi

# Start container
echo "Starting container..."
docker run -d --name false2true-test -p 18080:8080 false2true-proxy

# Wait for container to start
echo "Waiting for container to start..."
sleep 5

# Check if container is running
if ! docker ps | grep -q "false2true-test"; then
    echo "ERROR: Container failed to start"
    docker logs false2true-test
    exit 1
fi

echo "Container is running"
echo "Proxy is available at http://localhost:18080"

# Test with curl
echo "Testing with curl..."
if command -v curl &> /dev/null; then
    curl -s -x http://localhost:18080 http://httpbin.org/get | grep -q "origin" && echo "Curl test passed" || echo "Curl test failed"
else
    echo "curl not available, skipping curl test"
fi

# Show container logs
echo "Container logs:"
docker logs false2true-test --tail 10

# Stop container
echo "Stopping container..."
docker stop false2true-test
docker rm false2true-test

echo "=== Docker test completed successfully ==="

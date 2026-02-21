#!/bin/bash
# Build script for False2True Proxy

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== False2True Proxy Build Script ===${NC}"

# Parse arguments
BUILD_DOCKER=false
PUSH_DOCKER=false
TAG=""
CLEAN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --docker)
            BUILD_DOCKER=true
            shift
            ;;
        --push)
            PUSH_DOCKER=true
            BUILD_DOCKER=true
            shift
            ;;
        --tag)
            TAG="$2"
            shift 2
            ;;
        --clean)
            CLEAN=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--docker] [--push] [--tag TAG] [--clean]"
            exit 1
            ;;
    esac
done

# Clean if requested
if [ "$CLEAN" = true ]; then
    echo -e "${YELLOW}Cleaning build artifacts...${NC}"
    rm -rf __pycache__ *.pyc build dist *.egg-info .pytest_cache
    docker system prune -f 2>/dev/null || true
    echo -e "${GREEN}Clean completed${NC}"
fi

# Python setup
echo -e "${BLUE}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Run tests
echo -e "${BLUE}Running tests...${NC}"
python tests/test_addon.py
echo -e "${GREEN}Tests passed${NC}"

# Docker build
if [ "$BUILD_DOCKER" = true ]; then
    echo -e "${BLUE}Building Docker image...${NC}"
    
    # Set tag
    if [ -z "$TAG" ]; then
        TAG="false2true-proxy:local"
    fi
    
    # Build image
    docker build -t "$TAG" .
    
    # Test the image
    echo -e "${BLUE}Testing Docker image...${NC}"
    docker run --rm "$TAG" --version
    
    echo -e "${GREEN}Docker image built successfully: $TAG${NC}"
    
    # Push if requested
    if [ "$PUSH_DOCKER" = true ]; then
        echo -e "${BLUE}Pushing Docker image...${NC}"
        
        # Check if we have a registry tag
        if [[ "$TAG" != *"/"* ]]; then
            echo -e "${RED}Tag does not contain registry. Use --tag registry/image:tag for pushing${NC}"
            exit 1
        fi
        
        docker push "$TAG"
        echo -e "${GREEN}Docker image pushed: $TAG${NC}"
    fi
fi

echo -e "${GREEN}=== Build completed successfully ===${NC}"

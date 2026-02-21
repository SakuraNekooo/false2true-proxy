# Contributing to False2True Proxy

Thank you for your interest in contributing! Here are some guidelines to help you get started.

## How to Contribute

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/false2true-proxy.git
   cd false2true-proxy
   ```
3. **Create a new branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and test them
5. **Commit your changes** with descriptive messages:
   ```bash
   git commit -m "Add feature: your feature description"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request** on the original repository

## Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .  # Install in development mode
   ```

2. Run tests:
   ```bash
   python -m pytest tests/
   ```

3. Test the addon:
   ```bash
   mitmdump -s mitm_false2true.py
   ```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where appropriate
- Add docstrings to functions and classes
- Write tests for new features

## Reporting Issues

When reporting issues, please include:

1. A clear, descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Environment details (Python version, mitmproxy version, OS)
6. Any relevant logs or error messages

## Feature Requests

Feature requests are welcome! Please:

1. Check if the feature already exists or has been requested
2. Explain the use case clearly
3. Describe the expected behavior

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

# False2True Proxy

A MITMProxy addon that automatically replaces `false` with `true` in HTTP responses. Useful for testing, debugging, or having some fun with web applications.

## Features

- 🔄 Replaces `false` with `true` in HTTP responses
- 🎯 Smart content-type detection (JSON, HTML, JavaScript, XML, etc.)
- 🛡️ Preserves JSON structure when possible
- 📊 Logging and statistics
- 🚫 Skips binary content (images, videos, etc.)
- 🔧 Configurable via command-line options

## Installation

### Prerequisites
- Python 3.7+
- pip

### Install from source
```bash
git clone https://github.com/yourusername/false2true-proxy.git
cd false2true-proxy
pip install -r requirements.txt
```

### Quick install
```bash
pip install mitmproxy
```

## Usage

### Basic usage
```bash
mitmdump -s mitm_false2true.py
```

### With mitmproxy (interactive)
```bash
mitmproxy -s mitm_false2true.py
```

### Set proxy in your browser or system
1. Configure your browser/system to use the proxy at `127.0.0.1:8080`
2. Install the MITMProxy CA certificate (mitmproxy will guide you)
3. Start browsing - all `false` values will become `true`!

### Advanced options
```bash
# Run on a different port
mitmdump -s mitm_false2true.py --listen-port 8888

# Verbose logging
mitmdump -s mitm_false2true.py -v

# Save modified traffic to file
mitmdump -s mitm_false2true.py -w modified_traffic.mitm
```

## How It Works

The addon intercepts HTTP responses and:
1. Checks if the content-type is text-based (JSON, HTML, JS, XML, etc.)
2. Decodes the response content
3. Replaces all occurrences of `false` with `true` (and `False` with `True`)
4. For JSON responses, it also converts boolean `false` to `true`
5. Returns the modified response to the client

## Examples

### Before (JSON response):
```json
{
  "success": false,
  "enabled": false,
  "count": 0,
  "message": "Operation failed",
  "items": []
}
```

### After modification:
```json
{
  "success": true,
  "enabled": true,
  "count": 0,
  "message": "Operation failed",
  "items": []
}
```

### Before (JavaScript):
```javascript
var isReady = false;
var hasError = false;
```

### After modification:
```javascript
var isReady = true;
var hasError = true;
```

## Use Cases

- 🧪 Testing how applications behave when APIs always return `true`
- 🐛 Debugging optimistic UI states
- 🎭 Pranks (use responsibly!)
- 🔬 Research on client-side validation
- 🛠️ Development and prototyping

## Configuration

### Environment Variables
- `FALSE2TRUE_PORT` - Proxy port (default: 8080)
- `FALSE2TRUE_VERBOSE` - Enable verbose logging

### Content Types Processed
By default, the addon processes these content types:
- `text/*` (all text types)
- `application/json`
- `application/javascript`
- `application/xml`
- `application/xhtml+xml`

## Project Structure

```
false2true-proxy/
├── mitm_false2true.py    # Main MITMProxy addon
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .gitignore           # Git ignore file
├── examples/            # Example configurations
│   ├── custom_rules.py  # Example of custom rules
│   └── test_server.py   # Simple test server
└── tests/               # Test files
    └── test_addon.py    # Unit tests
```

## Development

### Running tests
```bash
python -m pytest tests/
```

### Adding new features
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code style
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions and classes

## Security Considerations

⚠️ **Important**: This tool modifies network traffic. Use responsibly:

1. **Only use on networks and applications you own or have permission to test**
2. **The MITMProxy CA certificate must be installed in the client browser/device**
3. **This will break SSL/TLS verification unless the certificate is trusted**
4. **Some applications may behave unexpectedly when `false` becomes `true`**

## Troubleshooting

### "Certificate error" in browser
Run MITMProxy and follow the instructions to install its CA certificate.

### Addon not modifying responses
1. Check that the proxy is correctly configured
2. Verify the content-type is being processed
3. Enable verbose logging with `-v`

### Performance issues
The addon adds minimal overhead. For high-traffic scenarios, consider:
- Using `mitmdump` instead of `mitmproxy` (non-interactive)
- Adding domain whitelisting in the code

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [MITMProxy](https://mitmproxy.org/) for the amazing proxy framework
- All contributors and users of this project

---

**Note**: This tool is for educational and testing purposes only. Use responsibly and with proper authorization.

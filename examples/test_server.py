#!/usr/bin/env python3
"""
Simple test server that returns responses with false values.
Use this to test the False2True proxy.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time

class TestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/api/json':
            self.send_json_response()
        elif self.path == '/api/text':
            self.send_text_response()
        elif self.path == '/api/javascript':
            self.send_javascript_response()
        elif self.path == '/':
            self.send_html_response()
        else:
            self.send_error(404, "Not Found")
    
    def send_json_response(self):
        data = {
            "status": "success",
            "enabled": False,
            "authenticated": False,
            "count": 3,
            "items": [
                {"id": 1, "active": False},
                {"id": 2, "active": False},
                {"id": 3, "active": True}
            ],
            "flags": {
                "feature_a": False,
                "feature_b": False,
                "feature_c": True
            },
            "message": "This contains false values"
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def send_text_response(self):
        text = """Status: false
Enabled: false
Ready: false
Complete: false
Error: false

All flags are currently false."""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(text.encode('utf-8'))
    
    def send_javascript_response(self):
        js = """
// Configuration
var config = {
    debug: false,
    verbose: false,
    enabled: false,
    features: {
        analytics: false,
        logging: false,
        cache: true
    }
};

// State
var isLoaded = false;
var hasError = false;
var isReady = false;

// Functions
function checkStatus() {
    return false;
}

function isEnabled() {
    return config.enabled;
}
"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/javascript')
        self.end_headers()
        self.wfile.write(js.encode('utf-8'))
    
    def send_html_response(self):
        html = """<!DOCTYPE html>
<html>
<head>
    <title>Test Server for False2True Proxy</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
        code { background: #eee; padding: 2px 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Test Server for False2True Proxy</h1>
        <p>This server returns responses containing <code>false</code> values.</p>
        
        <div class="endpoint">
            <h3>JSON Endpoint</h3>
            <p><code>GET /api/json</code> - Returns JSON with boolean false values</p>
            <a href="/api/json">Try it</a>
        </div>
        
        <div class="endpoint">
            <h3>Text Endpoint</h3>
            <p><code>GET /api/text</code> - Returns plain text with "false" strings</p>
            <a href="/api/text">Try it</a>
        </div>
        
        <div class="endpoint">
            <h3>JavaScript Endpoint</h3>
            <p><code>GET /api/javascript</code> - Returns JavaScript code with false values</p>
            <a href="/api/javascript">Try it</a>
        </div>
        
        <p>Configure your browser to use the False2True proxy at <code>127.0.0.1:8080</code> and reload this page to see the magic!</p>
    </div>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server(port=8000):
    server = HTTPServer(('localhost', port), TestHandler)
    print(f"Test server running on http://localhost:{port}")
    print("Endpoints:")
    print("  GET /              - HTML test page")
    print("  GET /api/json      - JSON response with false values")
    print("  GET /api/text      - Text response with false strings")
    print("  GET /api/javascript - JavaScript with false values")
    print("\nUse with False2True proxy: mitmdump -s ../mitm_false2true.py")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    run_server()

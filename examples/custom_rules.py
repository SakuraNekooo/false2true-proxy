#!/usr/bin/env python3
"""
Example of custom rules for the False2True addon.
This shows how to extend the basic functionality.
"""

from mitmproxy import http
import re

class CustomFalseToTrue:
    """
    Extended version with custom rules
    """
    
    def __init__(self):
        self.modified_count = 0
        
        # Custom patterns to replace (regex patterns)
        self.patterns = [
            (r'\bfalse\b', 'true'),      # word-boundary false
            (r'\bFalse\b', 'True'),      # word-boundary False
            (r'\bFALSE\b', 'TRUE'),      # word-boundary FALSE
            (r'"false"', '"true"'),      # quoted false
            (r':\s*false', ': true'),    # JSON-like false
            (r':\s*False', ': True'),    # JSON-like False
        ]
        
        # Domains to target (empty means all)
        self.target_domains = [
            # "api.example.com",
            # "test.example.org",
        ]
    
    def response(self, flow: http.HTTPFlow) -> None:
        # Domain filtering
        if self.target_domains:
            request_host = flow.request.host
            if not any(domain in request_host for domain in self.target_domains):
                return
        
        # Content type check
        content_type = flow.response.headers.get("content-type", "").lower()
        if not any(ct in content_type for ct in ["text/", "application/json", "application/javascript"]):
            return
        
        if not flow.response.content:
            return
        
        try:
            text = flow.response.content.decode('utf-8')
        except:
            return
        
        original_text = text
        
        # Apply all replacement patterns
        for pattern, replacement in self.patterns:
            text = re.sub(pattern, replacement, text)
        
        # Only update if changes were made
        if text != original_text:
            flow.response.content = text.encode('utf-8')
            self.modified_count += 1
            
            # Add custom header
            flow.response.headers["X-Custom-False2True"] = "modified"
    
    def done(self):
        print(f"CustomFalseToTrue: Modified {self.modified_count} responses")

# MITMProxy addon registration
addons = [CustomFalseToTrue()]

if __name__ == "__main__":
    print("Custom False2True example addon")
    print("Use: mitmdump -s examples/custom_rules.py")

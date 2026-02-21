#!/usr/bin/env python3
"""
MITMProxy addon to replace "false" with "true" in HTTP responses.
Usage: mitmdump -s mitm_false2true.py
"""

from mitmproxy import http
import re
import json
from typing import Union, Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FalseToTrue:
    """
    MITMProxy addon that replaces "false" with "true" in HTTP responses.
    Supports text, JSON, and other content types.
    """
    
    def __init__(self):
        self.modified_count = 0
        logger.info("FalseToTrue addon initialized")
    
    def response(self, flow: http.HTTPFlow) -> None:
        """
        Modify HTTP responses to replace "false" with "true"
        """
        # Skip non-text content types
        content_type = flow.response.headers.get("content-type", "").lower()
        
        # List of content types to process
        text_content_types = [
            "text/",
            "application/json",
            "application/javascript",
            "application/xml",
            "application/xhtml+xml",
            "application/x-www-form-urlencoded",
        ]
        
        # Check if we should process this content type
        should_process = any(ct in content_type for ct in text_content_types)
        
        if not should_process:
            return
        
        # Get the response content
        original_content = flow.response.content
        
        if not original_content:
            return
        
        # Try to decode as text
        try:
            # Try UTF-8 first
            text = original_content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                # Try other common encodings
                text = original_content.decode('latin-1')
            except:
                # If we can't decode, skip this response
                logger.debug(f"Cannot decode response with content-type: {content_type}")
                return
        
        # Count occurrences of "false"
        false_count = text.count('false')
        true_count = text.count('true')
        
        if false_count == 0:
            return
        
        # Replace "false" with "true" (case-sensitive)
        modified_text = text.replace('false', 'true')
        
        # Also replace "False" with "True" (for Python-style booleans)
        modified_text = modified_text.replace('False', 'True')
        
        # For JSON, we need to be more careful
        if 'application/json' in content_type:
            try:
                # Parse JSON to ensure we don't break the structure
                parsed = json.loads(text)
                modified_text = self._replace_in_json(parsed)
                modified_text = json.dumps(parsed, ensure_ascii=False)
            except json.JSONDecodeError:
                # If it's not valid JSON, use the simple replacement
                logger.debug("Content looks like JSON but is not valid, using simple replacement")
        
        # Update the response
        flow.response.content = modified_text.encode('utf-8')
        
        # Update statistics
        self.modified_count += 1
        new_true_count = modified_text.count('true')
        new_false_count = modified_text.count('false')
        
        logger.info(f"Modified response #{self.modified_count}: {flow.request.url}")
        logger.debug(f"  Changed: false:{false_count}->{new_false_count}, true:{true_count}->{new_true_count}")
        
        # Add a header to indicate modification
        flow.response.headers["X-False2True-Modified"] = "true"
        flow.response.headers["X-False2True-Changes"] = str(false_count)
    
    def _replace_in_json(self, obj: Any) -> Any:
        """
        Recursively replace false with true in JSON structures
        """
        if isinstance(obj, dict):
            return {k: self._replace_in_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._replace_in_json(item) for item in obj]
        elif obj is False:
            return True
        elif obj == "false":
            return "true"
        elif obj == "False":
            return "True"
        else:
            return obj
    
    def done(self):
        """Called when the proxy is shutting down"""
        logger.info(f"FalseToTrue addon finished. Modified {self.modified_count} responses.")

# Create an instance of our addon
addons = [FalseToTrue()]

if __name__ == "__main__":
    print("This is a MITMProxy addon script.")
    print("Run with: mitmdump -s mitm_false2true.py")
    print("Or: mitmproxy -s mitm_false2true.py")

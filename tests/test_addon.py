#!/usr/bin/env python3
"""
Simple tests for the False2True addon.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mitm_false2true import FalseToTrue
import json

def test_text_replacement():
    """Test basic text replacement"""
    addon = FalseToTrue()
    
    # Simulate a response
    class MockFlow:
        class Request:
            url = "http://example.com/test"
        class Response:
            headers = {"content-type": "text/plain"}
            content = b'{"status": false, "enabled": false}'
        
        request = Request()
        response = Response()
    
    flow = MockFlow()
    addon.response(flow)
    
    # Check the result
    result = flow.response.content.decode('utf-8')
    assert 'true' in result
    assert 'false' not in result
    print("✓ Text replacement test passed")

def test_json_replacement():
    """Test JSON boolean replacement"""
    addon = FalseToTrue()
    
    # Simulate a JSON response
    class MockFlow:
        class Request:
            url = "http://example.com/api"
        class Response:
            headers = {"content-type": "application/json"}
            content = json.dumps({
                "success": False,
                "enabled": False,
                "count": 0,
                "nested": {
                    "active": False,
                    "ready": False
                }
            }).encode('utf-8')
        
        request = Request()
        response = Response()
    
    flow = MockFlow()
    addon.response(flow)
    
    # Parse and check the result
    result = json.loads(flow.response.content.decode('utf-8'))
    assert result["success"] == True
    assert result["enabled"] == True
    assert result["nested"]["active"] == True
    assert result["nested"]["ready"] == True
    print("✓ JSON replacement test passed")

def test_skip_binary():
    """Test that binary content is skipped"""
    addon = FalseToTrue()
    
    class MockFlow:
        class Request:
            url = "http://example.com/image.png"
        class Response:
            headers = {"content-type": "image/png"}
            content = b'\x89PNG\r\n\x1a\n' + b'false' * 10
        
        request = Request()
        response = Response()
    
    original_content = MockFlow.response.content
    flow = MockFlow()
    addon.response(flow)
    
    # Content should not be modified
    assert flow.response.content == original_content
    print("✓ Binary skip test passed")

if __name__ == "__main__":
    print("Running False2True tests...")
    test_text_replacement()
    test_json_replacement()
    test_skip_binary()
    print("\nAll tests passed!")

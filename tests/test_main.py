import pytest
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Leantime MCP Server is running"}

def test_tools_endpoint():
    """Test that the tools endpoint returns a list of available tools."""
    response = client.get("/tools")
    assert response.status_code == 200
    response_data = response.json()
    assert "tools" in response_data
    assert isinstance(response_data["tools"], list)
    # Verify that at least one tool is included
    assert len(response_data["tools"]) > 0
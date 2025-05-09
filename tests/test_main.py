import pytest
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Leantime MCP Server is running"}

def test_execute_tool():
    tool_name = "test_tool"
    request_data = {
        "name": tool_name,
        "input": {"param1": "value1", "param2": "value2"}
    }
    
    response = client.post(f"/tools/{tool_name}", json=request_data)
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["output"]["status"] == "success"
    assert response_data["output"]["tool"] == tool_name
    assert response_data["output"]["input"] == request_data["input"]
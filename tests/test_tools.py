import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.app.tools.projects import ListProjectsTool, GetProjectTool, CreateProjectTool
from src.app.tools.tasks import ListTasksTool, GetTaskTool, CreateTaskTool, UpdateTaskTool
from src.app.services.leantime_client import LeantimeClient


@pytest.fixture
def mock_leantime_client():
    """Create a mock Leantime client."""
    client = AsyncMock(spec=LeantimeClient)
    return client


@pytest.mark.asyncio
async def test_list_projects_tool(mock_leantime_client):
    """Test the ListProjectsTool."""
    # Setup
    mock_projects = [
        {"id": 1, "name": "Project 1", "description": "Description 1"},
        {"id": 2, "name": "Project 2", "description": "Description 2"}
    ]
    mock_leantime_client.get_projects.return_value = mock_projects
    
    # Execute
    tool = ListProjectsTool(mock_leantime_client)
    result = await tool.run({})
    
    # Assert
    assert "projects" in result
    assert len(result["projects"]) == 2
    assert result["projects"] == mock_projects
    mock_leantime_client.get_projects.assert_called_once()


@pytest.mark.asyncio
async def test_get_project_tool(mock_leantime_client):
    """Test the GetProjectTool."""
    # Setup
    mock_project = {"id": 1, "name": "Project 1", "description": "Description 1"}
    mock_leantime_client.get_project.return_value = mock_project
    
    # Execute
    tool = GetProjectTool(mock_leantime_client)
    result = await tool.run({"project_id": 1})
    
    # Assert
    assert "project" in result
    assert result["project"] == mock_project
    mock_leantime_client.get_project.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_create_project_tool(mock_leantime_client):
    """Test the CreateProjectTool."""
    # Setup
    project_data = {
        "name": "New Project",
        "description": "New project description"
    }
    mock_project = {
        "id": 3,
        "name": "New Project",
        "description": "New project description"
    }
    mock_leantime_client.create_project.return_value = mock_project
    
    # Execute
    tool = CreateProjectTool(mock_leantime_client)
    result = await tool.run(project_data)
    
    # Assert
    assert "project" in result
    assert result["project"] == mock_project
    assert "message" in result
    mock_leantime_client.create_project.assert_called_once_with(project_data)


@pytest.mark.asyncio
async def test_list_tasks_tool(mock_leantime_client):
    """Test the ListTasksTool."""
    # Setup
    mock_tasks = [
        {"id": 1, "title": "Task 1", "projectId": 1},
        {"id": 2, "title": "Task 2", "projectId": 1}
    ]
    mock_leantime_client.get_tasks.return_value = mock_tasks
    
    # Execute
    tool = ListTasksTool(mock_leantime_client)
    result = await tool.run({"project_id": 1})
    
    # Assert
    assert "tasks" in result
    assert len(result["tasks"]) == 2
    assert result["tasks"] == mock_tasks
    mock_leantime_client.get_tasks.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_task_tool(mock_leantime_client):
    """Test the GetTaskTool."""
    # Setup
    mock_task = {"id": 1, "title": "Task 1", "projectId": 1}
    mock_leantime_client.get_task.return_value = mock_task
    
    # Execute
    tool = GetTaskTool(mock_leantime_client)
    result = await tool.run({"task_id": 1})
    
    # Assert
    assert "task" in result
    assert result["task"] == mock_task
    mock_leantime_client.get_task.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_create_task_tool(mock_leantime_client):
    """Test the CreateTaskTool."""
    # Setup
    task_data = {
        "title": "New Task",
        "projectId": 1,
        "description": "New task description"
    }
    mock_task = {
        "id": 3,
        "title": "New Task",
        "projectId": 1,
        "description": "New task description"
    }
    mock_leantime_client.create_task.return_value = mock_task
    
    # Execute
    tool = CreateTaskTool(mock_leantime_client)
    result = await tool.run(task_data)
    
    # Assert
    assert "task" in result
    assert result["task"] == mock_task
    assert "message" in result
    mock_leantime_client.create_task.assert_called_once_with(task_data)


@pytest.mark.asyncio
async def test_update_task_tool(mock_leantime_client):
    """Test the UpdateTaskTool."""
    # Setup
    task_data = {
        "task_id": 1,
        "title": "Updated Task",
        "description": "Updated task description"
    }
    expected_update_data = {
        "title": "Updated Task",
        "description": "Updated task description"
    }
    mock_task = {
        "id": 1,
        "title": "Updated Task",
        "projectId": 1,
        "description": "Updated task description"
    }
    mock_leantime_client.update_task.return_value = mock_task
    
    # Execute
    tool = UpdateTaskTool(mock_leantime_client)
    result = await tool.run(task_data)
    
    # Assert
    assert "task" in result
    assert result["task"] == mock_task
    assert "message" in result
    mock_leantime_client.update_task.assert_called_once_with(1, expected_update_data)
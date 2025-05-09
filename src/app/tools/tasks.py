from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from src.app.tools.base import BaseTool, ToolInput, ToolOutput
from src.app.services.leantime_client import LeantimeClient


class TaskData(BaseModel):
    """Model for task data."""
    id: int
    title: str
    description: Optional[str] = None
    projectId: int
    status: Optional[str] = None
    priority: Optional[str] = None
    assignedTo: Optional[int] = None
    startDate: Optional[str] = None
    dueDate: Optional[str] = None
    storyPoints: Optional[int] = None
    tags: Optional[List[str]] = None


class ListTasksInput(ToolInput):
    """Input model for listing tasks."""
    project_id: Optional[int] = Field(None, description="ID of the project to filter tasks by")


class ListTasksOutput(ToolOutput):
    """Output model for listing tasks."""
    tasks: List[TaskData]


class ListTasksTool(BaseTool):
    """Tool for listing tasks in Leantime."""
    
    name = "list_tasks"
    description = "Lists tasks in Leantime, optionally filtered by project"
    input_model = ListTasksInput
    output_model = ListTasksOutput
    
    def __init__(self, leantime_client: LeantimeClient):
        self.client = leantime_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool to list tasks."""
        tasks = await self.client.get_tasks(input_data.get("project_id"))
        
        # Format the response according to the output model
        return {
            "tasks": tasks
        }


class GetTaskInput(ToolInput):
    """Input model for getting a specific task."""
    task_id: int = Field(..., description="ID of the task to retrieve")


class GetTaskOutput(ToolOutput):
    """Output model for getting a specific task."""
    task: TaskData


class GetTaskTool(BaseTool):
    """Tool for getting details of a specific task in Leantime."""
    
    name = "get_task"
    description = "Gets details of a specific task in Leantime"
    input_model = GetTaskInput
    output_model = GetTaskOutput
    
    def __init__(self, leantime_client: LeantimeClient):
        self.client = leantime_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool to get a task."""
        task = await self.client.get_task(input_data["task_id"])
        
        # Format the response according to the output model
        return {
            "task": task
        }


class CreateTaskInput(ToolInput):
    """Input model for creating a task."""
    title: str = Field(..., description="Title of the task")
    description: Optional[str] = Field(None, description="Description of the task")
    projectId: int = Field(..., description="ID of the project")
    status: Optional[str] = Field(None, description="Status of the task")
    priority: Optional[str] = Field(None, description="Priority of the task")
    assignedTo: Optional[int] = Field(None, description="ID of the user the task is assigned to")
    startDate: Optional[str] = Field(None, description="Start date of the task (YYYY-MM-DD)")
    dueDate: Optional[str] = Field(None, description="Due date of the task (YYYY-MM-DD)")
    storyPoints: Optional[int] = Field(None, description="Story points of the task")
    tags: Optional[List[str]] = Field(None, description="Tags for the task")


class CreateTaskOutput(ToolOutput):
    """Output model for creating a task."""
    task: TaskData
    message: str = Field("Task created successfully")


class CreateTaskTool(BaseTool):
    """Tool for creating a new task in Leantime."""
    
    name = "create_task"
    description = "Creates a new task in Leantime"
    input_model = CreateTaskInput
    output_model = CreateTaskOutput
    
    def __init__(self, leantime_client: LeantimeClient):
        self.client = leantime_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool to create a task."""
        task = await self.client.create_task(input_data)
        
        # Format the response according to the output model
        return {
            "task": task,
            "message": "Task created successfully"
        }


class UpdateTaskInput(ToolInput):
    """Input model for updating a task."""
    task_id: int = Field(..., description="ID of the task to update")
    title: Optional[str] = Field(None, description="Title of the task")
    description: Optional[str] = Field(None, description="Description of the task")
    status: Optional[str] = Field(None, description="Status of the task")
    priority: Optional[str] = Field(None, description="Priority of the task")
    assignedTo: Optional[int] = Field(None, description="ID of the user the task is assigned to")
    startDate: Optional[str] = Field(None, description="Start date of the task (YYYY-MM-DD)")
    dueDate: Optional[str] = Field(None, description="Due date of the task (YYYY-MM-DD)")
    storyPoints: Optional[int] = Field(None, description="Story points of the task")


class UpdateTaskOutput(ToolOutput):
    """Output model for updating a task."""
    task: TaskData
    message: str = Field("Task updated successfully")


class UpdateTaskTool(BaseTool):
    """Tool for updating an existing task in Leantime."""
    
    name = "update_task"
    description = "Updates an existing task in Leantime"
    input_model = UpdateTaskInput
    output_model = UpdateTaskOutput
    
    def __init__(self, leantime_client: LeantimeClient):
        self.client = leantime_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool to update a task."""
        task_id = input_data.pop("task_id")
        task = await self.client.update_task(task_id, input_data)
        
        # Format the response according to the output model
        return {
            "task": task,
            "message": "Task updated successfully"
        }
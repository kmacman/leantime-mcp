from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from src.app.tools.base import BaseTool, ToolInput, ToolOutput
from src.app.services.leantime_client import LeantimeClient


class ListProjectsInput(ToolInput):
    """Input model for listing projects."""
    pass


class ProjectData(BaseModel):
    """Model for project data."""
    id: int
    name: str
    description: Optional[str] = None
    clientId: Optional[int] = None
    state: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None


class ListProjectsOutput(ToolOutput):
    """Output model for listing projects."""
    projects: List[ProjectData]


class ListProjectsTool(BaseTool):
    """Tool for listing all projects in Leantime."""
    
    name = "list_projects"
    description = "Lists all available projects in Leantime"
    input_model = ListProjectsInput
    output_model = ListProjectsOutput
    
    def __init__(self, leantime_client: LeantimeClient):
        self.client = leantime_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool to list projects."""
        projects = await self.client.get_projects()
        
        # Format the response according to the output model
        return {
            "projects": projects
        }


class GetProjectInput(ToolInput):
    """Input model for getting a specific project."""
    project_id: int = Field(..., description="ID of the project to retrieve")


class GetProjectOutput(ToolOutput):
    """Output model for getting a specific project."""
    project: ProjectData


class GetProjectTool(BaseTool):
    """Tool for getting details of a specific project in Leantime."""
    
    name = "get_project"
    description = "Gets details of a specific project in Leantime"
    input_model = GetProjectInput
    output_model = GetProjectOutput
    
    def __init__(self, leantime_client: LeantimeClient):
        self.client = leantime_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool to get a project."""
        project = await self.client.get_project(input_data["project_id"])
        
        # Format the response according to the output model
        return {
            "project": project
        }


class CreateProjectInput(ToolInput):
    """Input model for creating a project."""
    name: str = Field(..., description="Name of the project")
    description: Optional[str] = Field(None, description="Description of the project")
    clientId: Optional[int] = Field(None, description="ID of the client")
    startDate: Optional[str] = Field(None, description="Start date of the project (YYYY-MM-DD)")
    endDate: Optional[str] = Field(None, description="End date of the project (YYYY-MM-DD)")


class CreateProjectOutput(ToolOutput):
    """Output model for creating a project."""
    project: ProjectData
    message: str = Field("Project created successfully")


class CreateProjectTool(BaseTool):
    """Tool for creating a new project in Leantime."""
    
    name = "create_project"
    description = "Creates a new project in Leantime"
    input_model = CreateProjectInput
    output_model = CreateProjectOutput
    
    def __init__(self, leantime_client: LeantimeClient):
        self.client = leantime_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool to create a project."""
        project = await self.client.create_project(input_data)
        
        # Format the response according to the output model
        return {
            "project": project,
            "message": "Project created successfully"
        }
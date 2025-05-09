from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from src.app.tools.base import BaseTool, ToolInput, ToolOutput
from src.app.services.leantime_client import LeantimeClient


class TimesheetData(BaseModel):
    """Model for timesheet data."""
    id: int
    userId: int
    projectId: int
    ticketId: Optional[int] = None
    hours: float
    description: Optional[str] = None
    date: str


class ListTimesheetsInput(ToolInput):
    """Input model for listing timesheets."""
    user_id: Optional[int] = Field(None, description="ID of the user to filter timesheets by")
    project_id: Optional[int] = Field(None, description="ID of the project to filter timesheets by")
    task_id: Optional[int] = Field(None, description="ID of the task to filter timesheets by")


class ListTimesheetsOutput(ToolOutput):
    """Output model for listing timesheets."""
    timesheets: List[TimesheetData]


class ListTimesheetsTool(BaseTool):
    """Tool for listing timesheet entries in Leantime."""
    
    name = "list_timesheets"
    description = "Lists timesheet entries in Leantime, optionally filtered by user, project, or task"
    input_model = ListTimesheetsInput
    output_model = ListTimesheetsOutput
    
    def __init__(self, leantime_client: LeantimeClient):
        self.client = leantime_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool to list timesheet entries."""
        timesheets = await self.client.get_timesheets(
            user_id=input_data.get("user_id"),
            project_id=input_data.get("project_id"),
            task_id=input_data.get("task_id")
        )
        
        # Format the response according to the output model
        return {
            "timesheets": timesheets
        }


class CreateTimesheetInput(ToolInput):
    """Input model for creating a timesheet entry."""
    userId: int = Field(..., description="ID of the user")
    projectId: int = Field(..., description="ID of the project")
    ticketId: Optional[int] = Field(None, description="ID of the task (ticket)")
    hours: float = Field(..., description="Hours worked")
    description: Optional[str] = Field(None, description="Description of the work")
    date: str = Field(..., description="Date of the work (YYYY-MM-DD)")


class CreateTimesheetOutput(ToolOutput):
    """Output model for creating a timesheet entry."""
    timesheet: TimesheetData
    message: str = Field("Timesheet entry created successfully")


class CreateTimesheetTool(BaseTool):
    """Tool for creating a new timesheet entry in Leantime."""
    
    name = "create_timesheet"
    description = "Creates a new timesheet entry in Leantime"
    input_model = CreateTimesheetInput
    output_model = CreateTimesheetOutput
    
    def __init__(self, leantime_client: LeantimeClient):
        self.client = leantime_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool to create a timesheet entry."""
        timesheet = await self.client.create_timesheet(input_data)
        
        # Format the response according to the output model
        return {
            "timesheet": timesheet,
            "message": "Timesheet entry created successfully"
        }
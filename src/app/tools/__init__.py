from typing import Dict, List, Type
from src.app.tools.base import BaseTool

# Import tool implementations
from src.app.tools.projects import ListProjectsTool, GetProjectTool, CreateProjectTool
from src.app.tools.tasks import ListTasksTool, GetTaskTool, CreateTaskTool, UpdateTaskTool
from src.app.tools.users import ListUsersTool, GetUserTool
from src.app.tools.timesheets import ListTimesheetsTool, CreateTimesheetTool

# Register all available tools
AVAILABLE_TOOLS: Dict[str, Type[BaseTool]] = {
    # Projects
    "list_projects": ListProjectsTool,
    "get_project": GetProjectTool,
    "create_project": CreateProjectTool,
    
    # Tasks
    "list_tasks": ListTasksTool,
    "get_task": GetTaskTool,
    "create_task": CreateTaskTool,
    "update_task": UpdateTaskTool,
    
    # Users
    "list_users": ListUsersTool,
    "get_user": GetUserTool,
    
    # Timesheets
    "list_timesheets": ListTimesheetsTool,
    "create_timesheet": CreateTimesheetTool,
}
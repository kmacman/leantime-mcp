from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from src.app.tools.base import BaseTool, ToolInput, ToolOutput
from src.app.services.leantime_client import LeantimeClient


class UserData(BaseModel):
    """Model for user data."""
    id: int
    username: str
    email: str
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    role: Optional[str] = None
    status: Optional[str] = None


class ListUsersInput(ToolInput):
    """Input model for listing users."""
    pass


class ListUsersOutput(ToolOutput):
    """Output model for listing users."""
    users: List[UserData]


class ListUsersTool(BaseTool):
    """Tool for listing all users in Leantime."""
    
    name = "list_users"
    description = "Lists all users in Leantime"
    input_model = ListUsersInput
    output_model = ListUsersOutput
    
    def __init__(self, leantime_client: LeantimeClient):
        self.client = leantime_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool to list users."""
        users = await self.client.get_users()
        
        # Format the response according to the output model
        return {
            "users": users
        }


class GetUserInput(ToolInput):
    """Input model for getting a specific user."""
    user_id: int = Field(..., description="ID of the user to retrieve")


class GetUserOutput(ToolOutput):
    """Output model for getting a specific user."""
    user: UserData


class GetUserTool(BaseTool):
    """Tool for getting details of a specific user in Leantime."""
    
    name = "get_user"
    description = "Gets details of a specific user in Leantime"
    input_model = GetUserInput
    output_model = GetUserOutput
    
    def __init__(self, leantime_client: LeantimeClient):
        self.client = leantime_client
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool to get a user."""
        user = await self.client.get_user(input_data["user_id"])
        
        # Format the response according to the output model
        return {
            "user": user
        }
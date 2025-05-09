import httpx
from typing import Dict, Any, Optional, List, Union
import json
import os
from pydantic import BaseModel


class LeantimeClient:
    """Client for interacting with the Leantime API."""
    
    def __init__(self, base_url: str, api_key: str = None, username: str = None, password: str = None):
        """
        Initialize the Leantime API client.
        
        Args:
            base_url: Base URL of the Leantime instance (e.g., https://leantime.example.com)
            api_key: API key for authentication
            username: Username for basic authentication (used if API key not provided)
            password: Password for basic authentication (used if API key not provided)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.username = username
        self.password = password
        self.session = None
        self.headers = {}
        
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    async def __aenter__(self):
        """Set up async context manager."""
        self.session = httpx.AsyncClient(base_url=self.base_url, headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up async context manager."""
        if self.session:
            await self.session.aclose()
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make a request to the Leantime API.
        
        Args:
            method: HTTP method (get, post, put, delete)
            endpoint: API endpoint (without base URL)
            **kwargs: Additional parameters to pass to httpx
            
        Returns:
            API response data
        """
        if not self.session:
            raise RuntimeError("Client not initialized. Use with 'async with' context manager.")
            
        # Add basic auth if using username/password
        auth = None
        if not self.api_key and self.username and self.password:
            auth = (self.username, self.password)
            
        url = f"{endpoint}"
        response = await self.session.request(method, url, auth=auth, **kwargs)
        
        try:
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # Handle API errors
            error_detail = ""
            try:
                error_detail = response.json()
            except:
                error_detail = response.text
            
            raise Exception(f"Leantime API error: {e.response.status_code} - {error_detail}")
        except json.JSONDecodeError:
            # Handle non-JSON responses
            return {"text": response.text}
    
    # Projects
    async def get_projects(self) -> List[Dict[str, Any]]:
        """Get all projects."""
        return await self._request("GET", "/api/projects")
    
    async def get_project(self, project_id: int) -> Dict[str, Any]:
        """Get a specific project by ID."""
        return await self._request("GET", f"/api/projects/{project_id}")
    
    async def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project."""
        return await self._request("POST", "/api/projects", json=project_data)
    
    async def update_project(self, project_id: int, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing project."""
        return await self._request("PUT", f"/api/projects/{project_id}", json=project_data)
    
    # Tasks
    async def get_tasks(self, project_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get tasks, optionally filtered by project.
        
        Args:
            project_id: Optional project ID to filter tasks
            
        Returns:
            List of task objects
        """
        endpoint = "/api/tickets"
        params = {}
        if project_id:
            params["projectId"] = project_id
            
        return await self._request("GET", endpoint, params=params)
    
    async def get_task(self, task_id: int) -> Dict[str, Any]:
        """Get a specific task by ID."""
        return await self._request("GET", f"/api/tickets/{task_id}")
    
    async def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task."""
        return await self._request("POST", "/api/tickets", json=task_data)
    
    async def update_task(self, task_id: int, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing task."""
        return await self._request("PUT", f"/api/tickets/{task_id}", json=task_data)
    
    async def delete_task(self, task_id: int) -> Dict[str, Any]:
        """Delete a task."""
        return await self._request("DELETE", f"/api/tickets/{task_id}")
    
    # Milestones
    async def get_milestones(self, project_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get milestones, optionally filtered by project."""
        endpoint = "/api/milestones"
        params = {}
        if project_id:
            params["projectId"] = project_id
            
        return await self._request("GET", endpoint, params=params)
    
    # Users
    async def get_users(self) -> List[Dict[str, Any]]:
        """Get all users."""
        return await self._request("GET", "/api/users")
    
    async def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get a specific user by ID."""
        return await self._request("GET", f"/api/users/{user_id}")
    
    # Timesheets
    async def get_timesheets(self, 
                             user_id: Optional[int] = None,
                             project_id: Optional[int] = None,
                             task_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get timesheet entries, optionally filtered."""
        endpoint = "/api/timesheets"
        params = {}
        if user_id:
            params["userId"] = user_id
        if project_id:
            params["projectId"] = project_id
        if task_id:
            params["ticketId"] = task_id
            
        return await self._request("GET", endpoint, params=params)
    
    async def create_timesheet(self, timesheet_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new timesheet entry."""
        return await self._request("POST", "/api/timesheets", json=timesheet_data)
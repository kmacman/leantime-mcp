from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import os
import json

from src.app.services.leantime_client import LeantimeClient
from src.app.tools import AVAILABLE_TOOLS
from src.app.tools.base import BaseTool

# Configuration
LEANTIME_URL = os.getenv("LEANTIME_URL", "")
LEANTIME_API_KEY = os.getenv("LEANTIME_API_KEY", "")
LEANTIME_USERNAME = os.getenv("LEANTIME_USERNAME", "")
LEANTIME_PASSWORD = os.getenv("LEANTIME_PASSWORD", "")

app = FastAPI(title="Leantime MCP Server")


class ToolRequest(BaseModel):
    name: str
    input: Dict[str, Any]


class ToolResponse(BaseModel):
    output: Dict[str, Any]


async def get_leantime_client():
    """Create and return a Leantime client."""
    client = LeantimeClient(
        base_url=LEANTIME_URL,
        api_key=LEANTIME_API_KEY if LEANTIME_API_KEY else None,
        username=LEANTIME_USERNAME if not LEANTIME_API_KEY and LEANTIME_USERNAME else None,
        password=LEANTIME_PASSWORD if not LEANTIME_API_KEY and LEANTIME_PASSWORD else None,
    )
    
    async with client:
        yield client


@app.get("/")
async def root():
    """Root endpoint to check if the server is running."""
    return {"message": "Leantime MCP Server is running"}


@app.get("/tools")
async def list_tools():
    """List all available tools."""
    tools_info = []
    
    for tool_name, tool_class in AVAILABLE_TOOLS.items():
        tools_info.append({
            "name": tool_name,
            "description": tool_class.description
        })
    
    return {"tools": tools_info}


@app.post("/tools/{tool_name}", response_model=ToolResponse)
async def execute_tool(
    tool_name: str, 
    request: ToolRequest,
    leantime_client: LeantimeClient = Depends(get_leantime_client)
):
    """Execute a specific tool."""
    if tool_name not in AVAILABLE_TOOLS:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    try:
        # Initialize the tool with the Leantime client
        tool_class = AVAILABLE_TOOLS[tool_name]
        tool_instance = tool_class(leantime_client)
        
        # Run the tool
        result = await tool_instance.run(request.input)
        
        return ToolResponse(output=result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch")
async def execute_batch(
    requests: List[ToolRequest],
    leantime_client: LeantimeClient = Depends(get_leantime_client)
):
    """Execute multiple tools in a batch."""
    results = []
    
    for request in requests:
        if request.name not in AVAILABLE_TOOLS:
            raise HTTPException(status_code=404, detail=f"Tool '{request.name}' not found")
        
        try:
            # Initialize the tool with the Leantime client
            tool_class = AVAILABLE_TOOLS[request.name]
            tool_instance = tool_class(leantime_client)
            
            # Run the tool
            result = await tool_instance.run(request.input)
            
            results.append({
                "tool": request.name,
                "output": result
            })
            
        except Exception as e:
            results.append({
                "tool": request.name,
                "error": str(e)
            })
    
    return {"results": results}
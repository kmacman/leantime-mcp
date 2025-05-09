# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy .env example and configure it
cp .env.example .env
# Update .env with your Leantime instance details
```

### Running the Server

```bash
# Start the MCP server
python run.py
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tools.py

# Run specific test
pytest tests/test_tools.py::test_list_projects_tool
```

## Architecture

The Leantime MCP Server is a FastAPI-based application that provides an interface for Claude to interact with Leantime (a project management system) through its API. The server follows the Model-Control-Provider (MCP) protocol for integration with Claude.

### Key Components

1. **FastAPI Application** (`src/app/main.py`): 
   - Defines the API endpoints
   - Handles request/response routing
   - Manages dependency injection

2. **Leantime Client** (`src/app/services/leantime_client.py`):
   - Provides an abstraction layer for the Leantime API
   - Handles authentication and request formatting
   - Implements methods for each Leantime API endpoint

3. **Tool System**:
   - Base Tool Class (`src/app/tools/base.py`): Defines the abstract interface for all tools
   - Specialized Tool Implementations:
     - Projects (`src/app/tools/projects.py`): Tools for managing Leantime projects
     - Tasks (`src/app/tools/tasks.py`): Tools for managing Leantime tasks
     - Users (`src/app/tools/users.py`): Tools for managing Leantime users
     - Timesheets (`src/app/tools/timesheets.py`): Tools for managing Leantime time entries

4. **Configuration** (`config/config.py`):
   - Loads environment variables using python-dotenv
   - Configures server settings and Leantime connection details

### Request Flow

1. The client makes a request to the MCP server (either directly or via Claude)
2. The FastAPI app routes the request to the appropriate endpoint
3. The endpoint creates a Leantime client instance
4. The appropriate tool is instantiated with the Leantime client
5. The tool validates the input data and executes its logic
6. The tool returns a response which is validated against its output model
7. The response is sent back to the client

### Tool Pattern

Each tool follows a consistent pattern:
1. Define input and output Pydantic models
2. Implement a tool class that inherits from `BaseTool`
3. Provide required class variables (name, description, input_model, output_model)
4. Implement the `execute` method containing the tool's logic

### Available Tools

- **Projects**: list_projects, get_project, create_project
- **Tasks**: list_tasks, get_task, create_task, update_task
- **Users**: list_users, get_user
- **Timesheets**: list_timesheets, create_timesheet
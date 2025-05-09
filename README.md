# Leantime MCP Server

A Python-based MCP (Model-Control-Provider) server for Leantime integration, providing tools to interact with a Leantime instance via its API.

## Features

- REST API for executing Leantime-related tools
- Tools for managing projects, tasks, users, and timesheets
- Batch execution support for multiple tools
- FastAPI-based with async request handling

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```
   cp .env.example .env
   ```
   Update the values with your Leantime instance information.

## Running the Server

Start the server with:
```
python run.py
```

The server will be available at `http://localhost:8000` by default.

## API Endpoints

- `GET /`: Check if the server is running
- `GET /tools`: List all available tools
- `POST /tools/{tool_name}`: Execute a specific tool
- `POST /batch`: Execute multiple tools in a batch

## Available Tools

### Projects
- `list_projects`: Lists all available projects in Leantime
- `get_project`: Gets details of a specific project in Leantime
- `create_project`: Creates a new project in Leantime

### Tasks
- `list_tasks`: Lists tasks in Leantime, optionally filtered by project
- `get_task`: Gets details of a specific task in Leantime
- `create_task`: Creates a new task in Leantime
- `update_task`: Updates an existing task in Leantime

### Users
- `list_users`: Lists all users in Leantime
- `get_user`: Gets details of a specific user in Leantime

### Timesheets
- `list_timesheets`: Lists timesheet entries in Leantime
- `create_timesheet`: Creates a new timesheet entry in Leantime

## Example Usage

### List Projects

```bash
curl -X POST "http://localhost:8000/tools/list_projects" \
     -H "Content-Type: application/json" \
     -d '{"name": "list_projects", "input": {}}'
```

### Create Task

```bash
curl -X POST "http://localhost:8000/tools/create_task" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "create_task", 
           "input": {
             "title": "New Task",
             "projectId": 1,
             "description": "This is a new task",
             "status": "new"
           }
         }'
```

### Batch Execution

```bash
curl -X POST "http://localhost:8000/batch" \
     -H "Content-Type: application/json" \
     -d '[
           {"name": "list_projects", "input": {}},
           {"name": "list_tasks", "input": {"project_id": 1}}
         ]'
```

## Development

### Project Structure

```
leantime-mcp/
├── config/             # Configuration settings
├── src/
│   └── app/            # Application code
│       ├── services/   # Services (e.g., Leantime API client)
│       └── tools/      # Tool implementations
├── tests/              # Test files
├── .env.example        # Example environment variables
├── requirements.txt    # Python dependencies
├── run.py              # Server entry point
└── README.md           # This file
```

### Testing

Run tests with:
```
pytest
```
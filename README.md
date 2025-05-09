# Leantime MCP Server

A Python-based MCP (Model-Control-Provider) server for Leantime integration, providing tools to interact with a Leantime instance via its API.

## Features

- REST API for executing Leantime-related tools
- Tools for managing projects, tasks, users, and timesheets
- Batch execution support for multiple tools
- FastAPI-based with async request handling
- Compatible with Claude's MCP protocol

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

## Claude MCP Configuration

To use this server with Claude, add the following to your Claude MCP configuration file:

```json
{
  "tools": [
    {
      "name": "leantime_list_projects",
      "description": "Lists all available projects in Leantime",
      "provider": {
        "type": "http",
        "url": "http://localhost:8000/tools/list_projects",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json"
        },
        "bodyTemplate": {
          "name": "list_projects",
          "input": "{{{parameters}}}"
        },
        "responseSchema": {
          "type": "object",
          "properties": {
            "output": {
              "type": "object",
              "properties": {
                "projects": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": { "type": "integer" },
                      "name": { "type": "string" },
                      "description": { "type": ["string", "null"] }
                    }
                  }
                }
              }
            }
          }
        }
      },
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    },
    {
      "name": "leantime_create_task",
      "description": "Creates a new task in Leantime",
      "provider": {
        "type": "http",
        "url": "http://localhost:8000/tools/create_task",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json"
        },
        "bodyTemplate": {
          "name": "create_task",
          "input": "{{{parameters}}}"
        }
      },
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "description": "Title of the task"
          },
          "projectId": {
            "type": "integer",
            "description": "ID of the project"
          },
          "description": {
            "type": "string",
            "description": "Description of the task"
          },
          "status": {
            "type": "string",
            "description": "Status of the task"
          }
        },
        "required": ["title", "projectId"]
      }
    }
  ]
}
```

You can add more tools following the same pattern for any of the available tools listed below. Make sure to update the URL if you're not running the server on the default port or if it's on a different machine.

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
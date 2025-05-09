import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Server configuration
HOST = os.getenv("MCP_HOST", "0.0.0.0")
PORT = int(os.getenv("MCP_PORT", "8000"))
DEBUG = os.getenv("MCP_DEBUG", "False").lower() == "true"

# API configuration
API_PREFIX = os.getenv("MCP_API_PREFIX", "/api/v1")

# Leantime configuration
LEANTIME_URL = os.getenv("LEANTIME_URL", "")
LEANTIME_API_KEY = os.getenv("LEANTIME_API_KEY", "")
LEANTIME_USERNAME = os.getenv("LEANTIME_USERNAME", "")
LEANTIME_PASSWORD = os.getenv("LEANTIME_PASSWORD", "")
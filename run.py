import uvicorn
from config.config import HOST, PORT, DEBUG

if __name__ == "__main__":
    uvicorn.run("src.app.main:app", host=HOST, port=PORT, reload=DEBUG)
from fastapi import FastAPI
import socket
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
  hostname = socket.gethostname()
  return {"message" : f"Hello, World from {hostname}!"}

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)
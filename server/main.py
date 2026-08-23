from fastapi import FastAPI
from server.auth.create_user import router as create_route

app = FastAPI()
app.include_router(create_route)

@app.get("/")
def main():
    return {"message": "Hello"}
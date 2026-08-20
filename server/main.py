from fastapi import FastAPI
from auth.create_user import router as create_route

app = FastAPI()
app.include_router(create_route)

@app.get("/")
def main():
    return {"message": "Hello"}
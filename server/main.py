from fastapi import FastAPI
from server.auth.create_user import router as create_route
from server.services.get_product import router as prod_router

app = FastAPI()
app.include_router(create_route)
app.include_router(prod_router)

@app.get("/")
def main():
    return {"message": "Hello"}
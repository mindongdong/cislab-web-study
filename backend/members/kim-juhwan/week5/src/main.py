from fastapi import FastAPI
from api import book, category

app = FastAPI()
app.include_router(book.router)
app.include_router(category.router)

@app.get("/")
def health_check_handler():
    return {"ping": "pong"}



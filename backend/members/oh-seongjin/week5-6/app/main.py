from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api.routes.books import router as books_router
from app.api.routes.categories import router as categories_router

app = FastAPI(title="Books API")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(categories_router)
app.include_router(books_router)

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/test")

@app.delete("/test")

@app.put("/test")

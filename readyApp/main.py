import uvicorn

from fastapi import FastAPI

from hotels import router as router_hotels

app = FastAPI()
app.include_router(router=router_hotels)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.0", port=8080, workers=5)

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def func():
    return "Hello, world"


import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.0", port=8080, reload=True)

import uvicorn

from .app import app


@app.get("/echo/{number}")
async def echo_int(number: int):
    app.log.info(f"Test logging info: echo {number}")
    app.log.warning(f"Test logging warning: echo {number}")
    app.log.error(f"Test logging error: echo {number}")
    return {"echo": number}


if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        reload=False,
        host="0.0.0.0",
        port=8000,
        timeout_graceful_shutdown=60 * 60 * 1,
    )

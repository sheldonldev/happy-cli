import time

import uvicorn
from fastapi import Request
from fastapi.responses import HTMLResponse
from temp_project.app import app


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Start-Time"] = str(start_time)
    end_time = time.perf_counter()
    response.headers["X-End-Time"] = str(end_time)
    process_time = end_time - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
async def app_home():
    return "This is Home Page."


@app.get("/test-log/{number}")
async def test_log(number: int):
    app.log.info(f"Test logging info: echo {number}")
    app.log.warning(f"Test logging warning: echo {number}")
    app.log.error(f"Test logging error: echo {number}")
    return {"echo": number}


@app.get("/docs", include_in_schema=False)
async def api_documentation(request: Request):
    return HTMLResponse(
        """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Elements in HTML</title>

    <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
  </head>
  <body>

    <elements-api
      apiDescriptionUrl="openapi.json"
      router="hash"
    />

  </body>
</html>"""
    )


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")

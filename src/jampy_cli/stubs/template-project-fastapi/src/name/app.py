from contextlib import asynccontextmanager

from decompress_archive import _cfg
from decompress_archive._log import log
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from util_common.uuid import UUID


class CustomFastAPI(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = log
        self.uuid_generator = UUID()

        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


@asynccontextmanager
async def lifespan(app: CustomFastAPI):
    app.log.info("Starting up resources...")
    for name in dir(_cfg):
        attr = getattr(_cfg, name)
        if name.isupper() and not callable(attr):
            print(f"{name}: {attr}")

    yield
    app.log.info("Shutting down resources...")


app = CustomFastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)

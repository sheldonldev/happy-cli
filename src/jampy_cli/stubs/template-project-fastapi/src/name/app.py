from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from temp_project import _cfg
from temp_project._log import log
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


for name in dir(_cfg):
    attr = getattr(_cfg, name)
    if name.isupper() and not callable(attr):
        print(f"{name}: {attr}")

app = CustomFastAPI(docs_url=None, redoc_url=None)

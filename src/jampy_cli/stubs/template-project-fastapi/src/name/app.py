import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from temp_project._cfg import RESOURCE_ROOT
from temp_project._log import log
from util_common.uuid import UUID

os.environ["RESOURCE_ROOT"] = RESOURCE_ROOT


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


app = CustomFastAPI()

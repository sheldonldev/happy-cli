from typing import Callable

from rich import print as rprint


class Notifier:
    @staticmethod
    def exited(notify_fn: Callable):
        notify_fn("Exited!")

    @staticmethod
    def exists(notify_fn: Callable, message: str):
        notify_fn(f"{message} already exists!")

    @staticmethod
    def not_exists(notify_fn: Callable, message: str):
        notify_fn(f"{message} not exists!")

    @staticmethod
    def create_success(notify_fn: Callable, message: str):
        notify_fn(f"{message} created successfully!")

    @staticmethod
    def update_success(notify_fn: Callable, message: str):
        notify_fn(f"{message} updated successfully!")

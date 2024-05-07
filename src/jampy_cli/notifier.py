from typing import Callable

from rich import print


class Notifier:
    @staticmethod
    def exited(notify_fn: Callable = print):
        notify_fn("Exited!")

    @staticmethod
    def exists(message: str, notify_fn: Callable = print):
        notify_fn(f"{message} already exists!")

    @staticmethod
    def not_exists(message: str, notify_fn: Callable = print):
        notify_fn(f"{message} not exists!")

    @staticmethod
    def create_success(message: str, notify_fn: Callable = print):
        notify_fn(f"{message} created successfully!")

    @staticmethod
    def update_success(message: str, notify_fn: Callable = print):
        notify_fn(f"{message} updated successfully!")

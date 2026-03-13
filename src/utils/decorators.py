from __future__ import annotations

from typing import Callable
import logging


def input_error(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter the argument for the command."
        except KeyError:
            return "Contact not found."
        except Exception as e:
            logging.exception("Unexpected error occurred")
            return f"Unexpected error: {str(e)}"

    return inner
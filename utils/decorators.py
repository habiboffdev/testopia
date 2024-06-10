import inspect
from typing import Callable
from telebot.types import Message
def lock_non_registered(
    checker: Callable,
    default: Callable=None,
    users: Callable=None
    )->Callable:
    if not users:
        users = []
    def wrapper(method,):
        arg = "msg"
        arg_list = inspect.getfullargspec(method).args
        if arg in arg_list:
            def inner(message:Message,*args,**kwargs):
                if checker(message.from_user.id,users):
                    return method(message,*args,**kwargs)
                return default(message,*args,**kwargs) if default else None
            return inner
        return method
    return wrapper

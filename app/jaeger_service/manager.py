
from functools import wraps
import inspect
from typing import Callable
from .config import trace
from opentelemetry.sdk.trace import Span
from pydantic import BaseModel
from dataclasses import asdict, dataclass, is_dataclass
from json import dumps


def dependable_span(optional_name: str = "root_span"):
    def create_root_span():
        tracer = trace.get_tracer(__name__)
        root_span = tracer.start_as_current_span(
            name=optional_name or __name__)

        with root_span as current_span:

            yield current_span

    return create_root_span


def create_inside_span(optional_name: str = ""):

    tracer = trace.get_tracer(__name__)
    root_span = tracer.start_as_current_span(name=optional_name or __name__)

    with root_span as current_span:
        yield current_span


def create_span(optional_name: str = ""):

    tracer = trace.get_tracer(__name__)
    root_span = tracer.start_as_current_span(name=optional_name or __name__)

    return root_span


def process_args_kwargs(args: tuple, kwargs: dict, func: Callable, span: Span) -> dict:
    clean_data = {"body": []}
    for arg in args:
        if isinstance(arg, BaseModel):
            json_arg = arg.json()
        else:
            json_arg = dumps(asdict(arg))
        clean_data["body"].append(json_arg)

    for key, item in kwargs.items():

        if isinstance(item, BaseModel):
            json_arg = item.json()
        elif is_dataclass(item):
            json_arg = dumps(asdict(item))
        elif isinstance(item,  (str, int, float, bool)):
            json_arg = dumps({key: item})
        elif isinstance(item, (tuple, list, dict)):
            json_arg = dumps(item)

        else:
            continue
        clean_data["body"].append(json_arg)
    span.add_event(name=func.__name__, attributes=clean_data)
    return clean_data


def decorate_function_span(optional_name: str = ""):
    def decorator_func(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                with create_span(optional_name=optional_name) as span:
                    process_args_kwargs(args=args,
                                        kwargs=kwargs,
                                        func=func,
                                        span=span)
                    if inspect.iscoroutinefunction(func):
                        return await func(*args, **kwargs)
                    else:
                        return func(*args, **kwargs)

            except Exception as ex:
                raise ex
        return wrapper
    return decorator_func

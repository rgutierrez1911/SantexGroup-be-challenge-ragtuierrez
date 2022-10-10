import requests

from .manager import create_span


class JaegerRequestSession(requests.Session):
    def __init__(self) -> None:

        super().__init__()
        self.hooks["response"] = [self.add_jaeger_trace]

    def add_jaeger_trace(self, resp, *args, **kwargs):
        root_span = create_span(optional_name="request_call")
        with root_span as current_span:
            attributes = {}
            current_span.add_event(name="RequestCall", attributes=attributes)


req = JaegerRequestSession()

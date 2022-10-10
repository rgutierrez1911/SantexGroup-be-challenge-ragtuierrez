import time
from typing import Callable
from fastapi import Request

from app.jaeger_service.manager import create_span

from starlette.middleware.base import BaseHTTPMiddleware
from urllib.parse import urlparse
from urllib import parse
import json
from traceback import format_exc
from fastapi import Response
from opentelemetry.sdk.trace import Span
from opentelemetry.trace.status import Status, StatusCode


async def add_process_time_header(request: Request, call_next: Callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{str(process_time*1000)} ms"
    return response


async def set_body(request: Request, body: bytes):
    async def receive():  # -> Message:
        return {"type": "http.request", "body": body}
    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


async def process_response(

    request: Request,
    call_next: Callable,
    span: Span,
    name: str

):
    response: Response = await call_next(request)
    headers = dict(response.headers)
    if "json" not in headers["content-type"]:
        return response

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    resp_body = response_body.decode()
    span.add_event(name=f"{name} - output",
                   attributes={"response_body": resp_body})
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )


def generateStatus(
    status_code: int,
    description: str = None,

):
    if status_code == StatusCode.OK:
        description = None

    return Status(
        status_code=status_code,
        description=description
    )
    
async def generate_json_body (request:Request):
    headers = request.headers
    json_body = {}
    if "Content-Type" in headers:
        
        if "json" in headers["Content-Type"].lower():
            current_body = await get_body(request)
            json_body = json.loads(current_body)
        if "form" in headers["Content-Type"].lower():
            current_body = await get_body(request)
            json_body = parse.parse_qs(qs=current_body.decode())
    return json_body

async def add_jaeger_handler(request: Request, call_next: Callable):
    json_body = {}
    headers = request.headers

    query_params = dict(request.query_params)
    path_params = request.path_params
    json_body = generate_json_body(request=request)
    data = {
        "body": str(json_body),
        "query": str(query_params),
        "path_params": str(path_params),
        "headers": str(headers)
    }

    url_request = str(request.url.path)

    with create_span(optional_name=url_request) as current_span:
        current_span.add_event(name=f"{url_request} - input", attributes=data)

        try:

            response = await process_response(request=request,
                                              call_next=call_next,
                                              span=current_span,
                                              name=url_request)
            
            status = generateStatus(status_code=StatusCode.OK,
                                    description="Success")
            current_span.set_status(status=status)

            return response
        except Exception as ex:
            attributes = {"msg": format_exc()}
            current_span.add_event(name=ex.__class__.__name__,
                                   attributes=attributes)
            raise ex

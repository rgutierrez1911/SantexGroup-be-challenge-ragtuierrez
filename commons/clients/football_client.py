import asyncio
from typing import Callable, List
import requests as req
from requests.sessions import Session
from requests.exceptions import RequestException
from core.factories import settings
from urllib.parse import urljoin

from aiohttp.http_exceptions import HttpBadRequest
from fastapi.exceptions import HTTPException
import aiohttp 
import time
API_KEY: str = settings.API_KEY
BASE_URL_FOOTBAL: str = settings.BASE_URL_FOOTBAL

DEFAULT_HEADERS = {
    "X-Auth-Token": API_KEY
}


class ServerSession(Session):
  def __init__(self,
               prefix_url=None,
               additional_headers: dict = None,
               *args,
               **kwargs):

    super(ServerSession, self).__init__(*args, **kwargs)
    self.prefix_url = prefix_url
    if additional_headers:
      
      self.headers.update(**additional_headers)

  def request(self, method, url, *args, **kwargs)->dict:
    url = urljoin(self.prefix_url, url)
    resp = super(ServerSession, self).request(method, url, *args, **kwargs)

    if 200 <= resp.status_code < 400:
      return resp.json()
    raise RequestException(
        status="FAIL",
        message=resp.text
    )


client: Session = ServerSession(prefix_url=BASE_URL_FOOTBAL,
                                additional_headers=DEFAULT_HEADERS)



class AsyncSession:
  def __init__(self,
               prefix_url=None,
               additional_headers: dict = None,
               max_request_per_minute :int= 10,
               *args,
               **kwargs):
    
    self.max_request_per_minute:int = max_request_per_minute
    self.throttle_count:int = 0
    self.current_timestamp :int= None
    
    self.prefix_url = prefix_url
    self.aio_client = aiohttp.ClientSession(
        base_url=self.prefix_url,
        headers=additional_headers)
    
  def gather(self,*func:List[Callable]):
    num_requests=len(func)
    self.throttle_count+=num_requests
    if self.current_timestamp is None:
      self.current_timestamp = time.time()
    else:
      
      now = time.time()
      diff_seconds=now-self.current_timestamp
      
      if diff_seconds>60:
        self.throttle_count =0
        self.current_timestamp = None
      
      if diff_seconds<=60 and self.throttle_count >self.max_request_per_minute:
        raise HTTPException(status_code=401,detail=f"You have excedeed the max rate limit per minute : {self.max_request_per_minute} requests")

    
    
    return asyncio.gather(*func)
    

async_client = AsyncSession(prefix_url=BASE_URL_FOOTBAL,
                            additional_headers=DEFAULT_HEADERS)

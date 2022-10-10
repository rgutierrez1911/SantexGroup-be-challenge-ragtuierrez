from typing import Any
from pydantic import BaseModel


class BaseStorage(BaseModel):
    port: int = 6379
    host: str = "localhost"
    db : str = "0"
    connection: Any = None
    def connect(self): ...
    def close(self):...
    
    

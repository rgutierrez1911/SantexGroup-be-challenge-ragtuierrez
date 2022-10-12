from pydantic import BaseModel

class base(BaseModel):
  name :str

class out(BaseModel):
  message :str
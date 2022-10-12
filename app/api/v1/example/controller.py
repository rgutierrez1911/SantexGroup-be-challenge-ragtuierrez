from fastapi import APIRouter,Query
from .schema import *
from dependencies.user_dependencies import UserAccess, user_db_permitions

router = APIRouter()

tags = ["example"]
router.tags = tags

@router.post("/base", tags=tags , response_model=out)
async def ejecutor(args:base,
                   user_access: UserAccess = user_db_permitions(),
                   ):

  return {"message": "hola"}

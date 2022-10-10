from .schemas import DetailUserData, DetailUserDataPager, NewUser, ResponseUsuariosListDb, UserPermitionsDb
from fastapi import APIRouter , Depends
from core.general.schemas import Search, Success, SuccessCreated
from .services import (add_new_user, 
                       get_db_user_data, 
                       get_user_permitions_local, 
                       list_db_users,
                       get_user_list_bs
                       )

from dependencies.user_dependencies import user_token_data , UserAccess, user_db_permitions

router = APIRouter()

tags = ["USERS"]
router.tags = tags

@router.post("/new", response_model=Success, tags=tags)
def create_new_user(
    args : NewUser,
    user_access: UserAccess = user_db_permitions(permitions=["SHOW-USER"]),

):
    add_new_user(
        db = user_access.db,
        **args.dict()
    )
    user_access.db.commit()   
    return {"status" : "success"}


@router.get("/get_user_data/{id_user}" ,response_model=DetailUserData, tags=tags)
def get_user_detail_data(
    id_user:int,
    user_access : UserAccess =  user_db_permitions(permitions=[]),
):

    response = get_db_user_data(db=user_access.db, id_user=id_user)
    return response


@router.get("/list", tags=tags, response_model=ResponseUsuariosListDb)
async def list_users(
    user_access: UserAccess = user_token_data(),

):
    usuarios = list_db_users(db=user_access.db)
    return {"usuarios": usuarios}


@router.get("/user-permitions/{id_user}" ,response_model=UserPermitionsDb, tags=tags)
def get_user_detail_permitions_data(
    id_user:int,
    # user_access : UserAccess =  user_token_data_permitions(permitions=["LIST-USER" , "SHOW-USER"]),
    user_access: UserAccess = user_token_data(),
):
    
    user_permitions = get_user_permitions_local(
        db=user_access.db,
        id_user=id_user)

    return user_permitions

@router.get("/user-list" , response_model=DetailUserDataPager , tags=tags)
async def get_user_list(
     user_access: UserAccess = user_token_data(),
     args : Search = Depends(Search)
):
    
    user_paginated_data = get_user_list_bs(db=user_access.db,
                                           pag_actual=args.pag_actual,
                                           item_pagina=args.item_pagina)
    return user_paginated_data

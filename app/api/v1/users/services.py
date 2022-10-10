from typing import List
from .schemas import DetailUserDataPager, DetailUserPermitions
from .storage import get_user_list_db
from core.dbsetup import Grupo
from core.dbsetup import GrupoPermiso
from core.dbsetup import Permiso
from core.dbsetup import UsuarioGrupo
from commons.db_commons import  check_active_visible 
from core.dbsetup import Usuario , Colaborador , Session


common_filters = check_active_visible(Usuario,Colaborador) 
permition_filters = check_active_visible(UsuarioGrupo, GrupoPermiso, Grupo)
user_permition_filters = check_active_visible(UsuarioGrupo, GrupoPermiso, Grupo , Permiso)
user_group_permition_filters = check_active_visible(Usuario , Grupo , UsuarioGrupo)

usuario_colaborador_commons = [
    Usuario.name,
    Usuario.mail,
    Usuario.id_colaborador,
    Colaborador.id_jefatura,
    Colaborador.id_viceprecidencia,
    Colaborador.id_gerencia,
    Colaborador.id_cargo,
    Colaborador.gerencia,
    Colaborador.jefatura,
    Colaborador.viceprecidencia,
    Colaborador.cargo,
]
def add_new_user(
    db :Session,
    user_name :str ,
    first_name:str,
    last_name :str ,
    id_jefatura:int ,
    id_viceprecidencia:int ,
    id_gerencia:int ,
    id_cargo:int ,
    mail :str ,
    password:str

):
    new_colaborador = Colaborador(
        name=first_name,
        last_name=last_name,
        id_jefatura=id_jefatura,
        id_viceprecidencia=id_viceprecidencia,
        id_gerencia=id_gerencia,
        id_cargo=id_cargo,

    )
    db.add(new_colaborador)
    db.flush()

    new_user = Usuario(
        name=user_name,
        mail = mail,
        password = password, # XD
        access_type = "web",
        id_colaborador = new_colaborador.id,
        state = 1
    )
    
    db.add(new_user)
    db.flush()
    


def get_user_list (db:Session):
    
    user_data = db.query(
        Usuario
    ).join(
        UsuarioGrupo,
        UsuarioGrupo.id_usuario == Usuario.id,
    ).join(
        GrupoPermiso,
        GrupoPermiso.id_grupo == UsuarioGrupo.id_grupo,
    ).join(
        Grupo,
        Grupo.id == GrupoPermiso.id_permiso,
    ).filter(
        *permition_filters
    ).with_entities(
        UsuarioGrupo.id.label("id_usuario_grupo"),
        UsuarioGrupo.id_grupo,
        GrupoPermiso.id.label("id_grupo_permiso"),
        GrupoPermiso.id_permiso,
        Permiso.name,
    )
    return user_data
    

    
def get_db_user_data(
    db :Session,
    id_user:int,
):  

    user_data = db.query(
        Usuario
    ).join(
        Colaborador,
        Colaborador.id == Usuario.id_colaborador
    ).filter(
        Usuario.id == id_user,
        *common_filters,
    ).with_entities(
        *usuario_colaborador_commons
    ).first()._asdict()

    user_permitions = db.query(
        Usuario
    ).join(
        UsuarioGrupo,
        UsuarioGrupo.id_usuario == Usuario.id,
    ).join(
        GrupoPermiso,
        GrupoPermiso.id_grupo == UsuarioGrupo.id_grupo,
    ).join(
        Grupo,
        Grupo.id == GrupoPermiso.id_permiso,
    ).filter(
        *permition_filters,
        Usuario.id == id_user
    ).with_entities(
        UsuarioGrupo.id.label("id_usuario_grupo"),
        UsuarioGrupo.id_grupo,
        GrupoPermiso.id.label("id_grupo_permiso"),
        GrupoPermiso.id_permiso,
        Permiso.name,
    ).all()

    
    user_data["user_permitions"] = user_permitions

    return user_data


def list_db_users(
    db: Session,
):
    filtered_user_db = db.query(Usuario).filter(
        *common_filters,
    ).join(
        Colaborador,
        Colaborador.id == Usuario.id_colaborador
    ).with_entities(
        *usuario_colaborador_commons
    ).all()

    return filtered_user_db


def get_user_permitions_local (db: Session , id_user: int ):

    permition_query :List[Permiso] = db.query(
        Usuario
    ).join(
        UsuarioGrupo,UsuarioGrupo.id == Usuario.id
    ).join(
        GrupoPermiso,GrupoPermiso.id_grupo == UsuarioGrupo.id_grupo
    ).join(
        Permiso , Permiso.id == GrupoPermiso.id_permiso
    ).filter(
        *user_permition_filters,
        Usuario.id == id_user
    ).with_entities(
        Permiso.name
    ).all()
    current_permitions = [row.name for row in permition_query]
    return {"permitions" :current_permitions }


def get_user_admins(db:Session)->List[Usuario]:
    
    usuarios_admin=db.query(Usuario).join(
        UsuarioGrupo, 
        Usuario.id == UsuarioGrupo.id_usuario
    ).join(
        Grupo,
        Grupo.id  == UsuarioGrupo.id_grupo
    ).filter(
        *user_group_permition_filters,
        Grupo.name == "ADMIN"
    ).with_entities(
        Usuario.id,
        Usuario.name,
        Usuario.mail
    ).all()
    
    return usuarios_admin
    
def get_user_list_bs (db:Session ,
                      
                      pag_actual:int = 1,
                      item_pagina :int =10 ,
                      
                      ):
    db_sentence = get_user_list_db(db=db)
    current_pager = DetailUserDataPager(pag_actual=pag_actual,
                                        item_pagina=item_pagina)
    
    current_pager.paginate(db_sentence=db_sentence)
    

    return current_pager
    

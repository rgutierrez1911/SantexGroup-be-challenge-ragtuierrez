from sqlalchemy.orm import Session
from core.exceptions.auth import credentials_exception
from core.dbsetup import (Usuario,
                          UsuarioPermiso,
                          Permiso,
                          UsuarioGrupo,
                          GrupoPermiso,
                          Grupo,
                          Colaborador)

FIELDS_USUARIO = [
    Usuario.id ,
    Usuario.name ,
    Usuario.mail ,
    Usuario.hash_password   
]

FIELDS_COLABORADOR = [
    Colaborador.id_jefatura,
    Colaborador.id_gerencia,
    Colaborador.id_viceprecidencia,
    Colaborador.id_cargo,

    
    Colaborador.name.label("first_name"),
    Colaborador.last_name,

    Colaborador.jefatura,
    Colaborador.gerencia,
    Colaborador.viceprecidencia,
    Colaborador.cargo,
]

def search_user_db(db: Session, username: str)->Usuario:

    current_user= db.query(
        Usuario
    ).join(
        Colaborador, Colaborador.id == Usuario.id_colaborador
    ).filter(
        Usuario.active == True,
        Colaborador.active == True,
        Usuario.name == username,
    ).with_entities(
        *FIELDS_USUARIO,
        *FIELDS_COLABORADOR
    ).first()

    if not current_user:
        raise credentials_exception

    return current_user


def get_user_permitions(session: Session, id_usuario: int):
    

    user_permitions = session.query(
        Usuario
    ).join(
        UsuarioPermiso,
        UsuarioPermiso.id_usuario == Usuario.id
    ).join(
        Permiso,
        Permiso.id == UsuarioPermiso.id_permiso
    ).filter(
        Usuario.visible == True,
        UsuarioPermiso.active == True,
        Permiso.active == True,
        Usuario.id == id_usuario,
    ).with_entities(
        Permiso.name,
    ).order_by(
        Permiso.name.asc()
    ).all()

    group_permitions = session.query(
        UsuarioGrupo
    ).join(
        Usuario,
        Usuario.id == UsuarioGrupo.id_usuario
    ).join(
        Grupo, Grupo.id == UsuarioGrupo.id_grupo
    ).join(
        GrupoPermiso, GrupoPermiso.id_grupo == Grupo.id
    ).join(
        Permiso, Permiso.id == GrupoPermiso.id_permiso
    ).filter(
        UsuarioGrupo.id_usuario.in_([id_usuario]),
        UsuarioGrupo.active == True,
        Usuario.visible == True,
        Permiso.active == True,
        Grupo.active == True,
        GrupoPermiso.active == True,
    ).with_entities(
        Permiso.name,
    ).order_by(
        Permiso.name.asc()
    ).all()
    user_permitions = list(set([row.name for row in user_permitions]))
    group_permitions = list(set([row.name for row in group_permitions]))

    full_permitions = list(set([*user_permitions, *group_permitions]))

    return {
        "user_permitions": user_permitions,
        "group_permitions": group_permitions,
        "complete_permitions": full_permitions,

    }

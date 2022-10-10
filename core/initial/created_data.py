from core.extensions import  Session , session_decorator
from core.dbsetup import (Usuario,
                          Cargo,
                          Viceprecidencia,
                          Jefatura,
                          Gerencia, Colaborador,
                          Permiso,
                          Grupo,
                          GrupoPermiso,
                          UsuarioGrupo)
from db_orm_models.data.initial_data.base_users import *
from db_orm_models.data.initial_data.base_permitions import permisos  , grupo_admin , grupos_product


@session_decorator
def add_initial_data(db: Session = None):
    db_vp = Viceprecidencia(**new_vp)
    db_cargo = Cargo(**new_cargo)

    db.add(db_vp)
    db.add(db_cargo)

    db.flush()
    new_gerencia["id_viceprecidencia"] = db_vp.id
    db_gerencia = Gerencia(**new_gerencia)
    db.add(db_gerencia)
    db.flush()

    new_jefatura["id_gerencia"] = db_gerencia.id
    new_jefatura["id_viceprecidencia"] = db_vp.id
    db_jefatura = Jefatura(**new_jefatura)
    db.add(db_jefatura)
    db.flush()
    
    temp_dict = {
        "id_jefatura" : db_jefatura.id,
        "id_viceprecidencia" : db_vp.id,
        "id_gerencia" : db_gerencia.id,
        "id_cargo" : None
    }
    
    new_colaborador.update(temp_dict)
    test_usuario_colaborador.update(temp_dict)

    

    db_colaborador = Colaborador(**new_colaborador)
    db_colaborador_test = Colaborador(**test_usuario_colaborador)

    db.add(db_colaborador)
    db.add(db_colaborador_test)
    db.flush()

    new_usuario["id_colaborador"] = db_colaborador.id
    test_usuario["id_colaborador"] = db_colaborador_test.id

    db_usuario = Usuario(**new_usuario)
    db_usuario_test = Usuario(**test_usuario)
    
    db.add(db_usuario)
    db.add(db_usuario_test)
    db.flush()
    
    #! CREATE THE ASDMIN GROUP AND ADD 1 USER TO ADMIN
    new_admin_group = Grupo(name=grupo_admin)
    new_grupo_product = Grupo(name=grupos_product)
    db.add(new_admin_group)
    db.add(new_grupo_product)
    db.flush()

    admin_usuario_grupo = UsuarioGrupo(
        id_usuario=db_usuario.id,
        id_grupo=new_admin_group.id
    )
    admin_usuario_grupo_test = UsuarioGrupo(
        id_usuario=db_usuario_test.id,
        id_grupo=new_admin_group.id
    )
    
    db.add(admin_usuario_grupo)
    db.add(admin_usuario_grupo_test)
    db.flush()

    for permiso_db in permisos:

        new_permiso = Permiso(name=permiso_db)
        db.add(new_permiso)
        db.flush()
        grupo_permiso_db = GrupoPermiso(
            id_permiso=new_permiso.id,
            id_grupo=new_admin_group.id
        )
        db.add(grupo_permiso_db)
        db.flush()
    db.commit()

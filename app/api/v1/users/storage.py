from core.dbsetup import (Usuario,
                          Colaborador,
                          Session,
                          UsuarioGrupo,
                          GrupoPermiso,
                          Grupo,
                          )


from commons.db_commons import check_active_visible
common_filters = check_active_visible(Usuario,Colaborador) 

permition_filters = check_active_visible(UsuarioGrupo, GrupoPermiso, Grupo)
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

def get_user_list_db(db: Session):


    user_data = db.query(
        Usuario
    ).join(
        Colaborador,
        Colaborador.id == Usuario.id_colaborador
    ).filter(
        
        *common_filters,
    ).with_entities(
        *usuario_colaborador_commons
    )
    return user_data
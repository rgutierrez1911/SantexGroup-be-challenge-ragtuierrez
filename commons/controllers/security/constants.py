
from core.dbsetup import Usuario, Colaborador

FIELDS_TO_TOKEN = [
    "cargo",
    "correo",
    "gerencia",
    "id",
    "id_cargo",
    "cargo",
    "id_gerencia",
    "id_jefatura",
    "id_viceprecidencia",
    "jefatura",
    "nombre_completo",
    "permisos",
    "viceprecidencia",
    "nombre",
    "apellido",
]

FIELDS_FROM_USER_DB = [
    Usuario.id,
    Usuario.name,
    Usuario.mail,
    Usuario.state,
    Usuario.access_type,
    Usuario.active,
    (Colaborador.name + " " + Colaborador.last_name).label("full_name")
]

from core.extensions import base as Base
from db_orm_models.data import (

    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
    BigInteger,
    TIMESTAMP,
    Enum,
    Sequence,
    BOOLEAN,
    Numeric
)
from sqlalchemy import Identity 
from sqlalchemy.orm import Session

#? User Data for API permitions
from db_orm_models.data.jefatura import Jefatura
from db_orm_models.data.gerencia import Gerencia
from db_orm_models.data.viceprecidencia import Viceprecidencia
from db_orm_models.data.cargo import Cargo
from db_orm_models.data.colaborador import Colaborador

from db_orm_models.data.usuarios import Usuario

from db_orm_models.data.grupo import Grupo
from db_orm_models.data.usuario_grupo import UsuarioGrupo

from db_orm_models.data.grupo_permiso import GrupoPermiso
from db_orm_models.data.permiso import Permiso
from db_orm_models.data.usuario_permiso import UsuarioPermiso
from db_orm_models.data.products import Product
from db_orm_models.data.products_metrics import ProductsMetrics


from db_orm_models.data.user_subscribers import UserSubscribers
from db_orm_models.data.tweeters import Tweets

#! FOTBALL DB MODELS

from db_orm_models.data.football.competition import Competition
from db_orm_models.data.football.teams import Teams,TeamsCompetition
from db_orm_models.data.football.players import Players
from db_orm_models.data.football.players import Coachs

#! FOTBALL DB MODELS
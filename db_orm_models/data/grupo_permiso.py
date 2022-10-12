# write you database models in this file
from db_orm_models.data.common import CommonFields
from core.dbsetup import (
  Column,
  BigInteger,
  String,
  Integer,
  ForeignKey,
  Boolean,
  Float,
  TIMESTAMP,
  Enum,
  ForeignKey,
  Sequence
)

from core.extensions import base

class GrupoPermiso(CommonFields,base):
  __tablename__ = "tm_grupo_permiso"
  __table_args__ = {'comment': 'Tabla de datos de grupo permiso',}
  
  id_permiso = Column(Integer , ForeignKey("tm_permiso.id") , nullable=True ,comment = "Id permiso relacionado ")
  id_grupo = Column(Integer , ForeignKey("tm_grupo.id") , nullable=True ,comment = "Id grupo relacionado")


    
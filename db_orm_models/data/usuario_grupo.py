# write you database models in this file


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
from db_orm_models.data.common import CommonFields
from core.extensions import base

class UsuarioGrupo(CommonFields , base):
    __tablename__ = "tm_usuario_grupo"
    __table_args__ = {'comment': 'Tabla de datos de usuario grupo',}
   
    id_usuario = Column(Integer, ForeignKey("tm_usuario.id"), nullable=True, comment="Id de la del usuario relacionado")
    id_grupo =  Column(Integer , ForeignKey("tm_grupo.id") , nullable=True ,comment = "Id del grupo")
    

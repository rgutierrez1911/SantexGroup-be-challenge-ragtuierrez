"""base_tables

Revision ID: 85fcaeb0bf4c
Revises: 
Create Date: 2022-04-23 17:36:50.066354

"""
from alembic import op
import sqlalchemy as sa
from core.initial.created_data import add_initial_data

# revision identifiers, used by Alembic.
revision = '85fcaeb0bf4c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  print ("<<<<<<<<<<<<<<<<<<< PRIMER COMMIT <<<<<<<<<<<<<<<<<<<<<")
  print ("<<<<<<<<<<<<<<<<<<< PRIMER COMMIT <<<<<<<<<<<<<<<<<<<<<")
  # ### commands auto generated by Alembic - please adjust! ###
  op.create_table('tm_grupo',
  sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=1, cycle=True), autoincrement=True, nullable=False),
  sa.Column('register_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('modified_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('visible', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('name', sa.String(length=96), nullable=False),
  sa.PrimaryKeyConstraint('id'),
  comment='Tabla de datos de grupo'
  )
  op.create_table('tm_permiso',
  sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=1, cycle=True), autoincrement=True, nullable=False),
  sa.Column('register_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('modified_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('visible', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('name', sa.String(length=96), nullable=False),
  sa.Column('descripcion', sa.String(length=256), nullable=True),
  sa.PrimaryKeyConstraint('id'),
  comment='Tabla de datos de  permiso'
  )
  op.create_table('ts_cargo',
  sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=1, cycle=True), autoincrement=True, nullable=False),
  sa.Column('register_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('modified_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('visible', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('name', sa.String(length=96), nullable=False),
  sa.Column('jefatura', sa.Boolean(), server_default='false', nullable=True),
  sa.Column('gerencia', sa.Boolean(), server_default='false', nullable=True),
  sa.Column('viceprecidencia', sa.Boolean(), server_default='false', nullable=True),
  sa.PrimaryKeyConstraint('id'),
  comment='Tabla de datos de cargo'
  )
  op.create_table('ts_viceprecidencia',
  sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=1, cycle=True), autoincrement=True, nullable=False),
  sa.Column('register_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('modified_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('visible', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('name', sa.String(length=96), nullable=False),
  sa.PrimaryKeyConstraint('id'),
  comment='Tabla de datos de viceprecidencia'
  )
  op.create_table('tm_grupo_permiso',
  sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=1, cycle=True), autoincrement=True, nullable=False),
  sa.Column('register_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('modified_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('visible', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('id_permiso', sa.Integer(), nullable=True, comment='Id permiso relacionado '),
  sa.Column('id_grupo', sa.Integer(), nullable=True, comment='Id grupo relacionado'),
  sa.ForeignKeyConstraint(['id_grupo'], ['tm_grupo.id'], ),
  sa.ForeignKeyConstraint(['id_permiso'], ['tm_permiso.id'], ),
  sa.PrimaryKeyConstraint('id'),
  comment='Tabla de datos de grupo permiso'
  )
  op.create_table('ts_gerencia',
  sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=1, cycle=True), autoincrement=True, nullable=False),
  sa.Column('register_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('modified_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('visible', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('name', sa.String(length=96), nullable=False),
  sa.Column('tipo_gerencia', sa.String(length=128), nullable=True),
  sa.Column('id_viceprecidencia', sa.Integer(), nullable=True, comment='Id de la viceprecidencia de la gerencia '),
  sa.ForeignKeyConstraint(['id_viceprecidencia'], ['ts_viceprecidencia.id'], ),
  sa.PrimaryKeyConstraint('id'),
  comment='Tabla de datos de gerencia'
  )
  op.create_table('ts_jefatura',
  sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=1, cycle=True), autoincrement=True, nullable=False),
  sa.Column('register_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('modified_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('visible', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('name', sa.String(length=96), nullable=False),
  sa.Column('id_gerencia', sa.Integer(), nullable=True, comment='Id de la gerencia de la jefatura '),
  sa.Column('id_viceprecidencia', sa.Integer(), nullable=True),
  sa.ForeignKeyConstraint(['id_gerencia'], ['ts_gerencia.id'], ),
  sa.ForeignKeyConstraint(['id_viceprecidencia'], ['ts_viceprecidencia.id'], ),
  sa.PrimaryKeyConstraint('id'),
  comment='Tabla de datos de jefatura'
  )
  op.create_table('tm_colaborador',
  sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=1, cycle=True), autoincrement=True, nullable=False),
  sa.Column('register_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('modified_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('visible', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('name', sa.String(length=96), nullable=False),
  sa.Column('last_name', sa.String(length=128), nullable=False),
  sa.Column('id_jefatura', sa.Integer(), nullable=True, comment='Id de la jefatura del colaborador'),
  sa.Column('id_viceprecidencia', sa.Integer(), nullable=True, comment='Id de la Viceprecidencia'),
  sa.Column('id_gerencia', sa.Integer(), nullable=True, comment='Id de la Gerencia'),
  sa.Column('id_cargo', sa.Integer(), nullable=True),
  sa.ForeignKeyConstraint(['id_cargo'], ['ts_cargo.id'], ),
  sa.ForeignKeyConstraint(['id_gerencia'], ['ts_gerencia.id'], ),
  sa.ForeignKeyConstraint(['id_jefatura'], ['ts_jefatura.id'], ),
  sa.ForeignKeyConstraint(['id_viceprecidencia'], ['ts_viceprecidencia.id'], ),
  sa.PrimaryKeyConstraint('id'),
  comment='Tabla de datos de colaborador'
  )
  op.create_table('tm_usuario',
  sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=1, cycle=True), autoincrement=True, nullable=False),
  sa.Column('register_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('modified_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('visible', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('name', sa.String(length=256), nullable=False),
  sa.Column('mail', sa.String(length=256), nullable=False),
  sa.Column('hash_password', sa.String(length=512), nullable=True),
  sa.Column('state', sa.String(length=2), nullable=True),
  sa.Column('try_number', sa.Integer(), server_default='0', nullable=True),
  sa.Column('access_type', sa.String(length=16), nullable=True, comment='tipo de acceso del usuario'),
  sa.Column('id_colaborador', sa.Integer(), nullable=True),
  sa.ForeignKeyConstraint(['id_colaborador'], ['tm_colaborador.id'], ),
  sa.PrimaryKeyConstraint('id'),
  sa.UniqueConstraint('name'),
  comment='En esta tabla de usuarios registrados'
  )
  op.create_table('tm_usuario_grupo',
  sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=1, cycle=True), autoincrement=True, nullable=False),
  sa.Column('register_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('modified_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('visible', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('id_usuario', sa.Integer(), nullable=True, comment='Id de la del usuario relacionado'),
  sa.Column('id_grupo', sa.Integer(), nullable=True, comment='Id del grupo'),
  sa.ForeignKeyConstraint(['id_grupo'], ['tm_grupo.id'], ),
  sa.ForeignKeyConstraint(['id_usuario'], ['tm_usuario.id'], ),
  sa.PrimaryKeyConstraint('id'),
  comment='Tabla de datos de usuario grupo'
  )
  op.create_table('tm_usuario_permiso',
  sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=1, cycle=True), autoincrement=True, nullable=False),
  sa.Column('register_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('modified_date', sa.TIMESTAMP(), nullable=False),
  sa.Column('visible', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('active', sa.Boolean(), server_default='true', nullable=False),
  sa.Column('name', sa.String(length=96), nullable=False),
  sa.Column('id_usuario', sa.Integer(), nullable=True, comment='Id de  del usuario relacionado'),
  sa.Column('id_permiso', sa.Integer(), nullable=True, comment='Id del permiso relacionado'),
  sa.ForeignKeyConstraint(['id_permiso'], ['tm_permiso.id'], ),
  sa.ForeignKeyConstraint(['id_usuario'], ['tm_usuario.id'], ),
  sa.PrimaryKeyConstraint('id'),
  comment='Tabla de datos de  usuario_permiso'
  )
  # ### end Alembic commands ###
  print (f"<<<<<<<<<<<<<<<<<<< FIN PRIMER COMMIT {revision} <<<<<<<<<<<<<<<<<<<<<")
  op.execute("commit")
  add_initial_data()

def downgrade():
  # ### commands auto generated by Alembic - please adjust! ###
  op.drop_table('tm_usuario_permiso')
  op.drop_table('tm_usuario_grupo')
  op.drop_table('tm_usuario')
  op.drop_table('tm_colaborador')
  op.drop_table('ts_jefatura')
  op.drop_table('ts_gerencia')
  op.drop_table('tm_grupo_permiso')
  op.drop_table('ts_viceprecidencia')
  op.drop_table('ts_cargo')
  op.drop_table('tm_permiso')
  op.drop_table('tm_grupo')
  # ### end Alembic commands ###

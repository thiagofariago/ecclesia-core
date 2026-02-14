"""initial schema

Revision ID: 73a19a31178f
Revises: 
Create Date: 2026-02-14 16:37:57.486698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73a19a31178f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar tabela de usuários
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('senha_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('ADMIN', 'OPERADOR', name='roleenum'), nullable=False),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_ativo'), 'usuarios', ['ativo'], unique=False)
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)
    op.create_index(op.f('ix_usuarios_id'), 'usuarios', ['id'], unique=False)

    # Criar tabela de paróquias
    op.create_table(
        'paroquias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_paroquias_id'), 'paroquias', ['id'], unique=False)
    op.create_index(op.f('ix_paroquias_nome'), 'paroquias', ['nome'], unique=False)

    # Criar tabela de comunidades
    op.create_table(
        'comunidades',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('paroquia_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['paroquia_id'], ['paroquias.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comunidades_id'), 'comunidades', ['id'], unique=False)
    op.create_index(op.f('ix_comunidades_nome'), 'comunidades', ['nome'], unique=False)
    op.create_index(op.f('ix_comunidades_paroquia_id'), 'comunidades', ['paroquia_id'], unique=False)

    # Criar tabela de dizimistas
    op.create_table(
        'dizimistas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('comunidade_id', sa.Integer(), nullable=False),
        sa.Column('nome', sa.String(length=255), nullable=False),
        sa.Column('cpf', sa.String(length=14), nullable=True),
        sa.Column('telefone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('data_nascimento', sa.Date(), nullable=True),
        sa.Column('endereco', sa.Text(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['comunidade_id'], ['comunidades.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dizimistas_ativo'), 'dizimistas', ['ativo'], unique=False)
    op.create_index(op.f('ix_dizimistas_comunidade_id'), 'dizimistas', ['comunidade_id'], unique=False)
    op.create_index(op.f('ix_dizimistas_cpf'), 'dizimistas', ['cpf'], unique=True)
    op.create_index(op.f('ix_dizimistas_data_nascimento'), 'dizimistas', ['data_nascimento'], unique=False)
    op.create_index(op.f('ix_dizimistas_email'), 'dizimistas', ['email'], unique=False)
    op.create_index(op.f('ix_dizimistas_id'), 'dizimistas', ['id'], unique=False)
    op.create_index(op.f('ix_dizimistas_nome'), 'dizimistas', ['nome'], unique=False)
    op.create_index(op.f('ix_dizimistas_telefone'), 'dizimistas', ['telefone'], unique=False)

    # Criar tabela de contribuições
    op.create_table(
        'contribuicoes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('dizimista_id', sa.Integer(), nullable=True),
        sa.Column('comunidade_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.Enum('DIZIMO', 'OFERTA', name='tipocontribuicaoenum'), nullable=False),
        sa.Column('valor', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('data_contribuicao', sa.Date(), nullable=False),
        sa.Column('forma_pagamento', sa.String(length=100), nullable=True),
        sa.Column('referencia_mes', sa.String(length=7), nullable=True),
        sa.Column('observacoes', sa.Text(), nullable=True),
        sa.Column('criado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('atualizado_em', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['comunidade_id'], ['comunidades.id'], ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['dizimista_id'], ['dizimistas.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contribuicoes_comunidade_id'), 'contribuicoes', ['comunidade_id'], unique=False)
    op.create_index(op.f('ix_contribuicoes_data_contribuicao'), 'contribuicoes', ['data_contribuicao'], unique=False)
    op.create_index(op.f('ix_contribuicoes_dizimista_id'), 'contribuicoes', ['dizimista_id'], unique=False)
    op.create_index(op.f('ix_contribuicoes_id'), 'contribuicoes', ['id'], unique=False)
    op.create_index(op.f('ix_contribuicoes_referencia_mes'), 'contribuicoes', ['referencia_mes'], unique=False)
    op.create_index(op.f('ix_contribuicoes_tipo'), 'contribuicoes', ['tipo'], unique=False)


def downgrade() -> None:
    # Remover tabelas em ordem reversa (respeitando dependências)
    op.drop_index(op.f('ix_contribuicoes_tipo'), table_name='contribuicoes')
    op.drop_index(op.f('ix_contribuicoes_referencia_mes'), table_name='contribuicoes')
    op.drop_index(op.f('ix_contribuicoes_id'), table_name='contribuicoes')
    op.drop_index(op.f('ix_contribuicoes_dizimista_id'), table_name='contribuicoes')
    op.drop_index(op.f('ix_contribuicoes_data_contribuicao'), table_name='contribuicoes')
    op.drop_index(op.f('ix_contribuicoes_comunidade_id'), table_name='contribuicoes')
    op.drop_table('contribuicoes')

    op.drop_index(op.f('ix_dizimistas_telefone'), table_name='dizimistas')
    op.drop_index(op.f('ix_dizimistas_nome'), table_name='dizimistas')
    op.drop_index(op.f('ix_dizimistas_id'), table_name='dizimistas')
    op.drop_index(op.f('ix_dizimistas_email'), table_name='dizimistas')
    op.drop_index(op.f('ix_dizimistas_data_nascimento'), table_name='dizimistas')
    op.drop_index(op.f('ix_dizimistas_cpf'), table_name='dizimistas')
    op.drop_index(op.f('ix_dizimistas_comunidade_id'), table_name='dizimistas')
    op.drop_index(op.f('ix_dizimistas_ativo'), table_name='dizimistas')
    op.drop_table('dizimistas')

    op.drop_index(op.f('ix_comunidades_paroquia_id'), table_name='comunidades')
    op.drop_index(op.f('ix_comunidades_nome'), table_name='comunidades')
    op.drop_index(op.f('ix_comunidades_id'), table_name='comunidades')
    op.drop_table('comunidades')

    op.drop_index(op.f('ix_paroquias_nome'), table_name='paroquias')
    op.drop_index(op.f('ix_paroquias_id'), table_name='paroquias')
    op.drop_table('paroquias')

    op.drop_index(op.f('ix_usuarios_id'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    op.drop_index(op.f('ix_usuarios_ativo'), table_name='usuarios')
    op.drop_table('usuarios')

    # Remover enums
    sa.Enum('DIZIMO', 'OFERTA', name='tipocontribuicaoenum').drop(op.get_bind())
    sa.Enum('ADMIN', 'OPERADOR', name='roleenum').drop(op.get_bind())

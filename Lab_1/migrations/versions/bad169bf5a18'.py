"""empty message

Revision ID: 2cbd5ea64501
Revises: 
Create Date: 2020-12-07 01:24:08.050884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bad169bf5a18'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_users'], ['users.id'], ondelete='cascade'),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('count_of_users', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=70), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_users'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('email', sa.String(length=70), nullable=False),
    sa.Column('count_of_messages', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(length=70), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_table('history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('id_note', sa.Integer(), nullable=True),
    sa.Column('id_users', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=70), nullable=False),
    sa.Column('time_of_edit', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['id_note'], ['notes.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['id_users'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_note'),
    sa.UniqueConstraint('id_users'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=False),
    sa.Column('id_note', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=70), nullable=False),
    sa.ForeignKeyConstraint(['id_note'], ['notes.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_note'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.drop_table('history')
    op.drop_table('users')
    op.drop_table('notes')
    # ### end Alembic commands ###
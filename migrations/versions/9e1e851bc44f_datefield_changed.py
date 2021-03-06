"""datefield changed

Revision ID: 9e1e851bc44f
Revises: 50b73fd13529
Create Date: 2018-01-23 17:32:03.310516

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9e1e851bc44f'
down_revision = '50b73fd13529'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    #op.create_index(op.f('ix_AdminUser_username'), 'AdminUser', ['username'], unique=True)
    #op.drop_index('ix_AdminUser_username', table_name='AdminUser')
    op.add_column('posts', sa.Column('change_date', sa.DateTime(), nullable=True))
    op.add_column('posts', sa.Column('create_date', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_posts_title'), 'posts', ['title'], unique=True)
    op.drop_column('posts', 'date')
    op.create_index(op.f('ix_tags_name'), 'tags', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tags_name'), table_name='tags')
    op.add_column('posts', sa.Column('date', mysql.DATETIME(), nullable=True))
    op.drop_index(op.f('ix_posts_title'), table_name='posts')
    op.drop_column('posts', 'create_date')
    op.drop_column('posts', 'change_date')
    op.create_index('ix_AdminUser_username', 'AdminUser', ['username'], unique=True)
    op.drop_index(op.f('ix_AdminUser_username'), table_name='AdminUser')
    # ### end Alembic commands ###

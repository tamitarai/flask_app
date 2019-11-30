"""empty message

Revision ID: ea059009279c
Revises: 
Create Date: 2019-11-26 23:04:26.649076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea059009279c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=256), nullable=True),
    sa.Column('profile_image_url', sa.String(length=1024), nullable=True),
    sa.Column('date_published', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('answer_id', sa.Integer(), nullable=True),
    sa.Column('answer_image_url', sa.String(length=1024), nullable=True),
    sa.Column('answer_body', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['answer_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('language')
    op.drop_table('messages')
    op.add_column('user', sa.Column('date_published', sa.DateTime(), server_default='2019/11/26 14:04:26', nullable=True))
    op.add_column('user', sa.Column('twitter_id', sa.String(length=64), nullable=True))
    op.create_unique_constraint(None, 'user', ['twitter_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'twitter_id')
    op.drop_column('user', 'date_published')
    op.create_table('messages',
    sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('message', sa.VARCHAR(length=140), autoincrement=False, nullable=True)
    )
    op.create_table('language',
    sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
    sa.Column('developer', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True)
    )
    op.drop_table('question')
    # ### end Alembic commands ###

"""empty message

Revision ID: 88fa2e1b9449
Revises: d2f33981ab92
Create Date: 2019-12-08 19:50:34.242222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88fa2e1b9449'
down_revision = 'd2f33981ab92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('answerer_image_url', sa.String(length=1024), nullable=True))
    op.drop_column('question', 'answer_image_url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('answer_image_url', sa.VARCHAR(length=1024), autoincrement=False, nullable=True))
    op.drop_column('question', 'answerer_image_url')
    # ### end Alembic commands ###

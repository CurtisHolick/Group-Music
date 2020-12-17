"""playlists table

Revision ID: bef0ca0de2a8
Revises: 00f3d248b6a7
Create Date: 2018-04-23 20:22:48.603678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bef0ca0de2a8'
down_revision = '00f3d248b6a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('playlist', sa.Column('spotify_playlist_id', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('playlist', 'spotify_playlist_id')
    # ### end Alembic commands ###
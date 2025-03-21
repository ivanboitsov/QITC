"""add_oauth_fields_to_user

Revision ID: 902439599c98
Revises: 
Create Date: 2025-03-21 00:47:07.580856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '902439599c98'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('auth_provider', sa.String(), nullable=True))
    op.add_column('user', sa.Column('provider_user_id', sa.String(), nullable=True))
    op.add_column('user', sa.Column('provider_user_data', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'provider_user_data')
    op.drop_column('user', 'provider_user_id')
    op.drop_column('user', 'auth_provider')
    # ### end Alembic commands ###

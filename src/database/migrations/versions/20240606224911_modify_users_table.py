"""modify_users_table

Revision ID: 8e32f45e8099
Revises: 49172a6ca10d
Create Date: 2024-06-06 22:49:11.349167

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8e32f45e8099"
down_revision: Union[str, None] = "49172a6ca10d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user_social_accounts", "user_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.drop_column("users", "password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "password", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
    )
    op.alter_column(
        "user_social_accounts", "user_id", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###

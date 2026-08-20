"""initial schema

Revision ID: 0001_initial
"""
from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    from app.database import Base
    import app.models  # noqa: F401  注册模型到 Base.metadata

    Base.metadata.create_all(bind=op.get_bind())


def downgrade():
    from app.database import Base

    Base.metadata.drop_all(bind=op.get_bind())

"""Add formal user accounts without disturbing existing anonymous-user data."""
from alembic import op
from sqlalchemy import inspect, Boolean, Column, DateTime, String

revision = "0002_add_accounts"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade():
    if not inspect(op.get_bind()).has_table("accounts"):
        op.create_table("accounts", Column("id", String(64), primary_key=True), Column("email", String(320), nullable=False, unique=True), Column("password_hash", String(512), nullable=False), Column("display_name", String(100), nullable=False), Column("role", String(20), nullable=False), Column("is_active", Boolean(), nullable=False), Column("created_at", DateTime(timezone=True)), Column("last_login_at", DateTime(timezone=True)))
        op.create_index("ix_accounts_email", "accounts", ["email"])
        op.create_index("ix_accounts_role", "accounts", ["role"])
def downgrade():
    if inspect(op.get_bind()).has_table("accounts"): op.drop_table("accounts")

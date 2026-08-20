from alembic import context
from sqlalchemy import engine_from_config, pool

from app.config import get_settings
from app.database import Base
import app.models  # noqa: F401  导入以注册所有模型到 Base.metadata

config = context.config
target_metadata = Base.metadata

# 让迁移使用与运行时一致的 DATABASE_URL（来自 .env 或环境变量），
# 避免与 alembic.ini 中硬编码的 URL 脱节导致连接失败。
config.set_main_option("sqlalchemy.url", get_settings().database_url)


def run_migrations_offline():
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

"""开发环境专用的数据重置命令：清空所有业务表数据。

仅允许在 environment=development 下运行，且必须显式传入 --yes 才会真正执行。
清空后需要重新运行 generate_products.py 与 seed_database.py 恢复模拟数据。
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.config import get_settings
from app.database import Base, SessionLocal
import app.models  # noqa: F401 - register all ORM tables before clearing them

# 按外键依赖顺序排列，避免清空时触发约束冲突。
TABLES = [
    "user_behaviors",
    "recommendation_logs",
    "products",
    "user_preferences",
    "users",
    "platforms",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="清空开发数据库中的所有业务数据。")
    parser.add_argument("--yes", action="store_true", help="显式确认执行清空")
    args = parser.parse_args()

    settings = get_settings()
    if settings.environment != "development":
        raise SystemExit("reset_database 仅允许在 development 环境运行，当前环境为 %s。" % settings.environment)

    if not args.yes:
        print("未执行任何操作。该命令会清空所有业务数据，请追加 --yes 确认。")
        sys.exit(1)

    db = SessionLocal()
    try:
        for table in TABLES:
            db.execute(Base.metadata.tables[table].delete())
        db.commit()
        print("已清空：" + ", ".join(TABLES))
        print("下一步：python scripts/generate_products.py && python scripts/seed_database.py")
    finally:
        db.close()


if __name__ == "__main__":
    main()

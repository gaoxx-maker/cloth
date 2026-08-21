# Fashion Explorer MVP v0.2

探索型服装推荐的可运行工程骨架：FastAPI + SQLAlchemy/Alembic + PostgreSQL + Next.js。它使用文字商品卡片和 5000 条可再生模拟数据，验证“保留审美相关性的新奇推荐”是否提高探索行为。

## 本地运行（Windows，直接使用本机 PostgreSQL）

此项目不要求 Docker Desktop。本机已检测到 PostgreSQL 17 服务正在运行；`psql.exe` 位于 `C:\Program Files\PostgreSQL\17\bin\psql.exe`。

1. 使用 pgAdmin 的 Query Tool 或下列 PowerShell 命令，以 PostgreSQL 管理员身份创建一次开发账号和数据库（这不是建表；表由 Alembic 自动创建）：

   ```powershell
   & "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d postgres -c "CREATE USER fashion_explorer WITH PASSWORD '191216';"
   & "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d postgres -c "CREATE DATABASE fashion_explorer OWNER fashion_explorer;"
   ```

2. 复制 `.env.example` 为 `.env`，将 `CHANGE_ME` 替换为上一步密码。密码包含 `@`、`:`、`/` 时必须做 URL 编码。
3. 后端：`cd backend`，创建虚拟环境并安装 `pip install -r requirements.txt`；随后执行 `alembic upgrade head`、`python ../scripts/generate_products.py`、`python ../scripts/seed_database.py`、`uvicorn app.main:app --reload`。
4. 前端：另开终端，`cd frontend`，执行 `npm install`、`npm run dev`，浏览 `http://localhost:3000`。

若账号或数据库已经存在，跳过第 1 步。不要手动创建数据表或插入商品；migration 与脚本会完成这些工作。

API 文档位于 `http://localhost:8000/docs`。详细的替换点见 `docs/TODO.md`，完整的后续开发顺序、接口契约与验收方式见 `docs/development-handoff.md`，部署见 `docs/deployment.md`。

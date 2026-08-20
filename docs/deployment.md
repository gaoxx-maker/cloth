# 部署

开发机可以直接使用本机 PostgreSQL 服务，不依赖 Docker。先用 pgAdmin 或 `psql` 创建开发角色与空数据库，再将其连接串写入根目录 `.env` 的 `DATABASE_URL`；表结构必须由 `alembic upgrade head` 创建。

生产环境部署 PostgreSQL 后设置 `DATABASE_URL`，运行 `alembic upgrade head` 和数据生成/导入脚本。FastAPI 以 `uvicorn app.main:app` 启动，并在 `CORS_ORIGINS` 中加入前端域名。Next.js 设置 `NEXT_PUBLIC_API_URL` 为后端 HTTPS 地址后执行 `npm run build && npm start`。可分别使用 Vercel（前端）、Render/Railway/云服务器（后端）和托管 PostgreSQL。

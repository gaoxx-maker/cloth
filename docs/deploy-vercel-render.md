# 使用 Vercel + Render 部署

本项目采用 Vercel 托管 Next.js 前端，Render Blueprint 托管 FastAPI 与 PostgreSQL。部署时使用 GitHub 分支 `codex/multimerchant-catalog-ui`。

## 1. 部署后端与数据库到 Render

1. 在 Render Dashboard 选择 **New + → Blueprint**，连接仓库 `gaoxx-maker/cloth`。
2. 选择分支 `codex/multimerchant-catalog-ui`；Render 会读取根目录 `render.yaml` 并创建：
   - `fashion-explorer-api` Web Service；
   - `fashion-explorer-db` PostgreSQL 数据库。
3. 对 `CORS_ORIGINS` 的提示先填写 Vercel 域名的 JSON 数组，例如：

   ```text
   ["https://your-project.vercel.app"]
   ```

4. 等待部署完成，打开 `https://<render-service>.onrender.com/health`，应返回 `status: ok`。

Blueprint 会自动安装依赖、运行 Alembic、生成 5,400 条三商户模拟报价并启动 API。Render 的数据库连接串会自动注入，应用会把其 `postgresql://` 格式转换为 psycopg v3 所需的 SQLAlchemy URL。

## 2. 部署前端到 Vercel

1. 在 Vercel 选择 **Add New → Project** 并导入同一 GitHub 仓库与分支。
2. 将 **Root Directory** 设置为 `frontend`。
3. 在 Production 环境变量设置：

   ```text
   NEXT_PUBLIC_API_URL=https://<render-service>.onrender.com
   ```

4. 点击 Deploy。之后每次推送该分支，Vercel 会重新部署前端。

## 3. 联调检查

- 访问 Vercel 域名，首页应显示瀑布流商品。
- 点击商品进入详情页，确认显示三家模拟商户报价。
- 点击报价链接可进入对应模拟商户页。
- 点击详情页“喜欢”，再打开 `/experiment` 检查行为统计。

## 生产环境变量与安全

- `DATABASE_URL`：由 Render 从托管 PostgreSQL 注入，不要复制到 Git。
- `CORS_ORIGINS`：仅填写 Vercel 的 HTTPS 域名，使用 JSON 数组格式。
- `NEXT_PUBLIC_API_URL`：Vercel 前端唯一需要的公开变量，值为 Render 后端 HTTPS 地址。
- `JD_API_KEY` 等第三方密钥：若未来启用，只在 Render 环境变量中手动设置，绝不写入 `render.yaml`、Vercel 或前端代码。

## 成本与限制

`render.yaml` 使用 Render 的 `free` Web Service 和 PostgreSQL 计划，适合演示。免费实例可能休眠，首次请求会变慢；若用于稳定访问，应在 Render Dashboard 升级套餐。

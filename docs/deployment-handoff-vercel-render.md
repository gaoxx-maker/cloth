# Vercel + Render 部署复盘与交接

更新时间：2026-08-21

## 部署架构

| 部分 | 平台 | 线上地址/职责 |
| --- | --- | --- |
| 前端 | Vercel | `https://cloth-pr8o.vercel.app`，托管 Next.js 页面 |
| 后端 | Render Web Service | `https://fashion-explorer-api.onrender.com`，提供 FastAPI REST API |
| 数据库 | Render PostgreSQL | 存放商品、模拟商户报价、用户行为与推荐日志 |
| 代码分支 | GitHub | `codex/multimerchant-catalog-ui`，Render Blueprint 的部署来源 |

浏览器只访问 Vercel；Vercel 构建产物通过 `NEXT_PUBLIC_API_URL` 调用 Render API；Render API 使用托管 PostgreSQL。

## 部署操作流程

### 1. 推送部署分支

```powershell
git checkout codex/multimerchant-catalog-ui
git push origin codex/multimerchant-catalog-ui
```

确认分支包含根目录 `render.yaml` 与 `frontend/vercel.json`。

### 2. 在 Render 创建 Blueprint

1. Render Dashboard → **New + → Blueprint**。
2. 选择 GitHub 仓库 `gaoxx-maker/cloth` 与分支 `codex/multimerchant-catalog-ui`。
3. 确认 Blueprint 创建 `fashion-explorer-api` 和 `fashion-explorer-db`。
4. 在首次提示 `CORS_ORIGINS` 时可先填 `[]`，完成前端域名确定后再更新。
5. 部署完成后访问：

   ```text
   https://fashion-explorer-api.onrender.com/health
   ```

   预期返回 `{"status":"ok","environment":"production"}`。

### 3. 在 Vercel 部署前端

1. Vercel → **Add New → Project**，导入同一仓库。
2. Root Directory 设置为 `frontend`。
3. 在 **Environment Variables** 设置以下变量，并同时应用到 Production 和 Preview：

   ```text
   NEXT_PUBLIC_API_URL=https://fashion-explorer-api.onrender.com
   ```

4. 保存后必须在 **Deployments** 中对最新部署点击 **Redeploy**，因为 `NEXT_PUBLIC_*` 变量会在 Next.js 构建阶段写入浏览器代码。

### 4. 回填 Render 跨域配置

Render → `fashion-explorer-api` → **Environment**，设置：

```text
CORS_ORIGINS=["https://cloth-pr8o.vercel.app"]
```

保存后执行 **Manual Deploy → Deploy latest commit**，或等待自动部署。

### 5. 上线验收

- 打开 Vercel 首页，商品瀑布流应显示商品。
- 商品详情页应有京东、淘宝、拼多多三条模拟报价。
- 点击模拟商户报价可跳转到对应模拟商户页。
- 点击详情页“喜欢”，在实验数据页应能看到行为统计更新。
- 访问 `/health`、`/products?limit=1` 应返回 200。

## 本次部署问题与解决

| 问题 | 根因 | 解决方案 |
| --- | --- | --- |
| Blueprint 同步失败 | Render 免费账号已有一个免费 PostgreSQL，无法再创建第二个 | 删除确认无用的旧数据库 `cloth-db` 后重新同步；不要删除未知用途的数据库 |
| 免费层拒绝 `preDeployCommand` | Render Free Web Service 不支持该字段 | 将 Alembic、模拟数据生成和导入放入 `startCommand`，启动服务前执行 |
| 服务启动时报 `cors_origins` 解析错误 | Render 环境变量被 Pydantic 按复杂列表解析失败 | 配置改为接收字符串，并支持 JSON 数组和逗号分隔格式，再在应用中转换为列表 |
| Vercel 页面显示“共 0 件” | `NEXT_PUBLIC_API_URL` 被填写为文档示例 `https://你的-render-api.onrender.com` | 替换为真实地址 `https://fashion-explorer-api.onrender.com` 并 Redeploy |
| 后端可用但浏览器请求失败 | Render 未允许 Vercel 域名跨域访问 | 设置精确的 `CORS_ORIGINS` JSON 数组并重启后端 |

## 运维交接清单

### 日常发布

1. 在 `codex/multimerchant-catalog-ui` 完成改动、测试与推送。
2. Render 自动或手动部署最新提交。
3. Vercel 会为对应分支创建 Preview；若改动了 `NEXT_PUBLIC_*` 变量，必须手动 Redeploy。
4. 检查 Render Logs、`/health` 和前端核心路径。

### 故障排查顺序

1. 访问 Render `/health`，确认服务是否 Live。
2. 访问 Render `/products?limit=1`，确认数据库是否已有商品。
3. 查看 Vercel 中 `NEXT_PUBLIC_API_URL` 是否为真实 Render URL，而非示例字符串。
4. 确认 Render `CORS_ORIGINS` 包含当前 Vercel 域名。
5. 检查 Vercel 部署是否在变量更新后重新构建。

### 安全与成本

- 不提交 `.env`、数据库连接串或真实平台 API 密钥。
- `NEXT_PUBLIC_API_URL` 是公开地址，可以放在 Vercel；`DATABASE_URL` 仅由 Render 注入。
- Render 免费服务可能休眠，首次访问可能较慢；需要稳定响应时升级实例。
- 免费数据库数量受账号限制；删除数据库不可恢复，先确认资源用途。

## 关键配置文件

- `render.yaml`：Render Web Service、PostgreSQL、启动命令和环境变量。
- `frontend/vercel.json`：Next.js 构建命令。
- `backend/app/config.py`：Render PostgreSQL URL 与 CORS 环境变量兼容逻辑。
- `docs/deploy-vercel-render.md`：简明部署说明。

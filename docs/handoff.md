# Fashion Explorer 最新版本交接文档

更新时间：2026-09-10

## 1. 当前版本与代码状态

`main` 已合并最新推荐体验与账户功能。当前线上后端地址为：

```text
https://cloth-e6s0.onrender.com
```

技术栈：Next.js + TypeScript（Web）、FastAPI + SQLAlchemy（API）、Render PostgreSQL（数据库）。项目核心仍是验证“保留审美相关性的新奇服装推荐”是否提升浏览与喜欢行为。

本次合并包含：账户认证、喜欢列表、推荐模式重构、按季节的推荐元数据、用户反馈与推荐画像优化，以及 Render/Vercel 部署配置兼容。

## 2. 已完成能力

### Web 页面

| 路径 | 功能 |
| --- | --- |
| `/` | 搜索、平衡/传统/探索三种推荐模式、推荐批次浏览、上一批/下一批、商品预览喜欢/取消喜欢 |
| `/login` | 邮箱注册与登录，登录成功后保存访问令牌 |
| `/account` | 我的喜欢；可以取消喜欢并跳转商品详情 |
| `/product/[id]` | 商品详情、登录后的喜欢、三家模拟商户报价 |
| `/merchant/[platform]/[catalogId]` | 京东、淘宝、拼多多模拟商户落地页 |
| `/search` | 按品牌、风格、颜色、品类搜索 |
| `/experiment` | 喜欢率、探索商品喜欢率、浏览量、风格跨度、换一件使用率等实验指标 |

探索度数值滑杆已移除，改为三档推荐模式按钮：`traditional`、`balanced`、`explore`。首页会在当前页面内保存已加载批次，支持返回上一批；刷新页面后批次缓存会重置。

### 后端 API

| 接口 | 说明 |
| --- | --- |
| `POST /auth/register` | 注册并签发 JWT |
| `POST /auth/login` | 登录并签发 JWT |
| `GET /auth/me` | 当前登录账户 |
| `GET /users/me/likes` | 当前账户的喜欢商品 |
| `GET /users/me/preferences` | 当前账户偏好 |
| `POST /behaviors` | 写入浏览、喜欢、取消喜欢、跳过等行为；需要登录 |
| `GET /recommendations/feed` | 返回指定模式的推荐批次及季节元数据 |
| `POST /recommendations/replace` | 按相似、探索、不同方向替换商品 |
| `GET /products/{id}` | 商品与同款三商户报价 |
| `GET /search` | 商品搜索 |
| `GET /experiments/stats` | 推荐实验统计 |
| `GET /admin/users` | 管理员账户列表 |
| `PATCH /admin/users/{id}` | 管理员启用或停用账户 |

商品数据仍为 1,800 个基础商品与三商户模拟报价（共约 5,400 条）；真实京东来源只保留低频、缓存、后端受控的扩展入口。

## 3. 核心实现位置

- 账户模型与迁移：`backend/app/models/account.py`、`backend/alembic/versions/0002_add_accounts.py`
- 密码散列、JWT：`backend/app/security.py`
- 认证与管理员接口：`backend/app/api/auth.py`、`backend/app/api/admin.py`
- 行为、偏好、推荐：`backend/app/services/behavior_service.py`、`preference_service.py`、`recommendation_service.py`
- 打分与推荐模式：`backend/app/recommendation/scorer.py`、`engine.py`、`explorer.py`
- 首页与模式选择：`frontend/src/app/page.tsx`
- 登录与我的喜欢：`frontend/src/app/login/page.tsx`、`frontend/src/app/account/page.tsx`
- 浏览器令牌：`frontend/src/services/identity.ts`

## 4. 发布前必须完成

1. 在 Render 环境变量设置：

   ```text
   AUTH_SECRET_KEY=<至少32位随机值>
   AUTH_ACCESS_TOKEN_MINUTES=480
   CORS_ORIGINS=["<Vercel生产域名>"]
   ```

2. 如需创建管理员，额外设置 `BOOTSTRAP_ADMIN_EMAIL` 与 `BOOTSTRAP_ADMIN_CODE`；管理员创建完成后删除或清空注册码。
3. Render 发布后确认启动过程执行 `alembic upgrade head`，数据库应位于 `0002_add_accounts`。
4. Vercel 的 `NEXT_PUBLIC_API_URL` 必须为 `https://cloth-e6s0.onrender.com`，更新变量后必须重新部署前端。
5. 验收：注册、登录、喜欢、我的喜欢、取消喜欢、商品详情、推荐模式、搜索、实验数据，以及 `/health`。

不要将 `DATABASE_URL`、`AUTH_SECRET_KEY`、第三方 API Key 或管理员注册码写入 Git、前端代码或截图。

## 5. 已知限制与下一阶段

- 注册只校验邮箱格式，尚未做真实邮箱验证、忘记密码与重置密码。
- JWT 当前放在浏览器 localStorage；高安全需求应升级为短期 access token + HttpOnly refresh cookie。
- 注册、登录、行为接口应补充速率限制与自动化 API 测试。
- Render 免费实例可能休眠，首次访问会较慢。
- 真实商户数据仍未接入，现有报价为受控模拟数据。

## 6. Android 同步状态

Android 工程位于 `D:\Android\fasionexplor`，当前已能连接 API、展示推荐、搜索、详情、换一件和实验数据，并已生成 debug APK。

它仍对应旧版匿名推荐交互，**尚未同步本次 Web 账户升级**。后续 Android 开发应优先增加：邮箱注册/登录、JWT 保存与 `Authorization: Bearer` 请求头、我的喜欢页、取消喜欢、三档推荐模式按钮，以及批次翻页；同时移除旧的探索度滑杆。

## 7. 本地开发

```powershell
# 后端
cd backend
alembic upgrade head
uvicorn app.main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

后端 API 文档：`/docs`；健康检查：`/health`。

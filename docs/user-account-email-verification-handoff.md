# 用户账户与邮箱验证交接文档

## 1. 当前状态（本地未发布）

项目已完成第一阶段正式账户能力，代码目前在本地工作区，尚未提交、推送或部署。商品、匿名浏览和原有推荐逻辑仍保留；登录用户的行为改为由服务端令牌识别，客户端不能再伪造 `user_id`。

已实现的页面：

- `/login`：邮箱密码注册、登录；
- `/account`：登录用户的“我的喜欢”；
- `/product/[id]`：未登录点击喜欢会跳转登录，登录后写入喜欢行为。

已实现的接口：

| 接口 | 用途 | 是否需要登录 |
| --- | --- | --- |
| `POST /auth/register` | 注册并返回 JWT | 否 |
| `POST /auth/login` | 登录并返回 JWT | 否 |
| `GET /auth/me` | 当前账户资料 | 是 |
| `POST /behaviors` | 记录浏览/喜欢行为 | 是 |
| `GET /users/me/preferences` | 当前账户偏好 | 是 |
| `GET /users/me/likes` | 当前账户喜欢的商品 | 是 |
| `GET /admin/users` | 查询账户列表 | 管理员 |
| `PATCH /admin/users/{id}` | 启用/停用账户 | 管理员 |

## 2. 后端实现位置

- 账户表模型：`backend/app/models/account.py`
- 密码散列及 JWT：`backend/app/security.py`
- 登录注册路由：`backend/app/api/auth.py`
- 管理员路由：`backend/app/api/admin.py`
- 鉴权依赖：`backend/app/dependencies.py`
- 数据库迁移：`backend/alembic/versions/0002_add_accounts.py`
- 前端认证请求：`frontend/src/services/authApi.ts`
- 浏览器令牌存储：`frontend/src/services/identity.ts`

密码使用 Python 标准库 `scrypt` 散列；JWT 为 HS256，默认有效期 480 分钟。访问令牌当前保存在浏览器 `localStorage`。后续如果涉及高安全性场景，应调整为短期 access token + HttpOnly refresh cookie。

## 3. 数据库与本地验证

已在本地执行：

```powershell
cd D:\fasion-explorer\backend
..\.venv\Scripts\alembic.exe upgrade head
```

数据库版本已到 `0002_add_accounts (head)`。该迁移仅创建 `accounts` 表，不会删除原有商品、匿名用户、行为或推荐数据。

已通过：

- 前端 `npm run build`；
- 后端 Python 语法检查；
- 密码哈希与 JWT 创建/校验自检。

本机 `FastAPI TestClient` 未运行，因为当前虚拟环境缺少测试依赖 `httpx2`；这不影响应用运行，但建议后续补充 pytest/API 自动化测试。

## 4. 上线前必须配置

在 Render 的 Web Service → Environment 中新增：

```env
AUTH_SECRET_KEY=一段至少32字符的随机字符串
AUTH_ACCESS_TOKEN_MINUTES=480
BOOTSTRAP_ADMIN_EMAIL=你的管理员邮箱
BOOTSTRAP_ADMIN_CODE=首次管理员注册码
```

注意：生产环境未设置 `AUTH_SECRET_KEY` 时，注册/登录会明确拒绝签发令牌，避免使用开发默认密钥。设置环境变量后需手动 Deploy latest commit 或等待 GitHub 推送触发自动部署。

管理员创建方式：使用 `BOOTSTRAP_ADMIN_EMAIL` 注册，并在注册请求的 `bootstrap_admin_code` 中填写 `BOOTSTRAP_ADMIN_CODE`。目前网页注册页未暴露该字段；可用 Swagger `/docs`、API 工具，或后续补一个仅初始化期使用的管理员注册入口。管理员创建后建议清空 Render 中的 `BOOTSTRAP_ADMIN_CODE`。

## 5. 邮箱验证：下一阶段需求

当前注册仅校验邮箱格式，**尚未验证邮箱是否真实**。正式上线前应实现下列流程：

1. 注册创建 `is_email_verified=false` 的账户；
2. 生成 6 位验证码（或一次性验证链接），只存储验证码哈希；
3. 设置 10–15 分钟过期时间、发送次数与验证失败次数；
4. 通过邮件服务发送验证码；
5. `POST /auth/verify-email` 验证成功后标记账户；
6. 未验证用户禁止登录，或只允许完成验证、不允许喜欢及个性化推荐；
7. 增加 `POST /auth/resend-verification`、忘记密码和重置密码流程。

建议的新增表 `email_verification_tokens`：

| 字段 | 说明 |
| --- | --- |
| `id` | 主键 |
| `account_id` | 对应账户 |
| `code_hash` | 验证码哈希，不能明文保存 |
| `expires_at` | 过期时间 |
| `attempt_count` | 输入失败次数 |
| `sent_count` | 重发次数 |
| `consumed_at` | 验证成功时间 |

邮件服务可选阿里云邮件推送（国内）、Resend 或 SendGrid（海外/开发体验好）。真实发送前需准备发件域名并完成 SPF、DKIM 配置。密钥只放 Render 环境变量，不能提交至 `.env`、GitHub 或前端。

开发阶段可增加 `EMAIL_PROVIDER=console`：只把验证码写到 Render 日志；切换生产邮件服务后再改为真实发送。

## 6. 推荐的后续开发顺序

1. 提交并推送当前账户功能，确认 Render 数据库迁移成功；
2. 配置 `AUTH_SECRET_KEY`，手工完成注册、登录、喜欢、喜欢列表验收；
3. 接入邮件服务和邮箱验证码；
4. 增加找回密码、改邮箱、登出、注销账户；
5. 增加管理员网页 `/admin`，调用现有管理员接口；
6. 为注册、登录、验证、权限拦截补充自动化测试和限流。

## 7. 安全检查清单

- 不在前端暴露邮件 API Key、数据库连接串或 `AUTH_SECRET_KEY`；
- 生产环境仅允许 Vercel 域名写入 CORS；
- 密码至少 8 位，后续可增加强度提示与常见弱密码拦截；
- 对注册、登录、验证码发送、验证码验证增加 IP 与邮箱限流；
- 管理员接口始终要求 JWT 中的 `role=admin`；
- 账户停用后，已有令牌在下一次请求时会被拒绝；
- 任何验证码和重置令牌均只保存哈希值，并保证可过期、一次性使用。

# Fashion Explorer 项目交接文档

更新时间：2026-08-21

## 项目定位

Fashion Explorer 是一个服装探索型推荐 Web 应用。它以本地生成的模拟商品为主，通过用户的浏览、打开详情和喜欢行为更新偏好，再按照探索度返回兼顾相关性与新颖度的推荐结果。

当前工作区包含 v0.2 标签之后的未提交功能：瀑布流商品展示、同款多商户模拟报价、商品详情页与模拟商户落地页。

## 技术结构

| 层级 | 技术/目录 | 职责 |
| --- | --- | --- |
| 前端 | `frontend/`，Next.js 15、React、TypeScript | 首页推荐、搜索、商品详情、模拟商户页、实验数据页 |
| 后端 | `backend/`，FastAPI、SQLAlchemy、PostgreSQL | 商品、推荐、行为、搜索与实验统计 REST API |
| 数据脚本 | `scripts/` | 生成模拟数据、导入数据库、重置开发数据 |
| 文档 | `docs/` | 架构、部署、数据库与交接信息 |

浏览器只请求 FastAPI；浏览器不会持有第三方 API 密钥。真实供应商接口应放在 `backend/app/integrations/` 中实现。

## 当前功能

- 首页以多列瀑布流展示推荐商品，点击卡片进入详情页。
- 首页“换一批”重新请求推荐流；探索度与推荐模式会影响排序。
- 商品详情页记录 `open_detail`，并提供单独的“喜欢”按钮记录 `like`。
- 同一基础商品有京东、淘宝、拼多多三条模拟报价；详情页列出价格并可跳转到对应的模拟商户页。
- 搜索结果只展示每个基础商品的一条代表报价，避免同款重复占据列表。
- 搜索、商品详情、模拟商户页、实验页带有返回按钮。
- 京东真实 API 集成仅保留低频 Provider 框架，默认关闭；没有完整的京东开放平台凭据时不会发起请求。

## 模拟商户数据

`scripts/generate_products.py` 生成 1,800 个基础商品，每个商品生成 3 条报价，共 5,400 条：

| 模拟商户 | 平台代码 | 定价系数 |
| --- | --- | --- |
| 京东模拟店 | `jd` | 1.00 |
| 淘宝模拟店 | `taobao` | 0.96 |
| 拼多多模拟店 | `pdd` | 0.91 |

同款关系不新增数据库列，而是编码在 `products.external_product_id` 中：`mock-00001:jd`、`mock-00001:taobao`、`mock-00001:pdd`。商品详情 API 按冒号前的 catalog ID 查出同组报价。

数据文件 `data/mock_products.json` 被 Git 忽略，可随时重新生成。

## 本地运行

先确保 PostgreSQL 已启动，且根目录 `.env` 的 `DATABASE_URL` 正确。

```powershell
cd D:\fasion-explorer
.\.venv\Scripts\python.exe -m alembic -c backend\alembic.ini upgrade head
.\.venv\Scripts\python.exe scripts\generate_products.py
.\.venv\Scripts\python.exe scripts\seed_database.py
```

启动后端：

```powershell
cd D:\fasion-explorer\backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

启动前端：

```powershell
cd D:\fasion-explorer\frontend
npm install
npm run dev
```

应用地址为 `http://localhost:3000`，后端 API 文档为 `http://localhost:8000/docs`。

## 重建开发数据

以下命令会删除本地开发库中的商品、用户行为、偏好和推荐日志，再写入新模拟数据：

```powershell
cd D:\fasion-explorer
.\.venv\Scripts\python.exe scripts\reset_database.py --yes
.\.venv\Scripts\python.exe scripts\generate_products.py
.\.venv\Scripts\python.exe scripts\seed_database.py
```

`reset_database.py` 仅允许 `ENVIRONMENT=development` 时执行。

## 关键 API

| API | 用途 |
| --- | --- |
| `GET /recommendations/feed` | 获取首页推荐列表 |
| `GET /search?q=...` | 搜索代表商品 |
| `GET /products/{id}` | 获取商品详情及同款商户报价 `offers` |
| `GET /products/merchant/{platform}/{catalogId}` | 获取模拟商户落地页商品 |
| `POST /behaviors` | 写入 `impression`、`open_detail`、`like` 等行为 |
| `GET /experiments/stats` | 查看实验统计 |

## 关键实现位置

- `backend/app/repositories/product_repository.py`：代表商品过滤、同款报价查询。
- `backend/app/services/product_service.py`：详情页 `offers` 响应组装。
- `scripts/generate_products.py`：多商户模拟数据生成。
- `scripts/seed_database.py`：创建平台并写入报价。
- `frontend/src/components/ProductFeed.tsx`：瀑布流商品列表。
- `frontend/src/app/product/[id]/page.tsx`：详情、喜欢和报价链接。
- `frontend/src/app/merchant/[platform]/[catalogId]/page.tsx`：模拟商户页。

## 已知限制与后续建议

1. 模拟商品尚未提供真实图片；前端会显示纹理化服装占位框。接入合规图片数据后可写入 `image_url`。
2. 真实京东开放平台调用需要可确认的 `app_key`、`app_secret`、`access_token`、签名规则和 SKU 来源；不要将这些写入前端或提交到 Git。
3. 当前同款关系通过字符串约定维护。生产化时建议新增独立 `catalog_products` 与 `merchant_offers` 表，并为报价增加更新时间、库存与来源字段。
4. 当前“换一批”依赖数据库随机候选抽样；若需要可复现实验，应按用户和 session 使用确定性随机种子。
5. 当前工作区包含未提交功能改动；交接前建议完成代码审查、补充 API 测试后再创建新版本提交。

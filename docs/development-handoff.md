# 后续开发交接指南

本文档定义 V0.1 骨架之后的实现边界、推荐开发顺序和验收条件。目标始终是验证探索型推荐是否提升浏览意愿；不要在本阶段加入支付、真实商品抓取、图片、Embedding 或复杂登录。

## 当前可用能力

| 模块 | 当前状态 | 说明 |
| --- | --- | --- |
| 商品 | 可用 | PostgreSQL Model、列表、详情、关键词搜索、5000 条生成器 |
| 匿名用户 | 可用 | 前端 localStorage UUID；后端首次行为/偏好请求时创建 |
| 行为记录 | 可用 | like/dislike/skip/replace 等事件可入库；like/dislike 会更新属性偏好 |
| Feed | 可用 | 支持 baseline、balanced、explore 与探索度参数 |
| 换一件 | 基础可用 | 按 similar/explore/different 过滤，尚未记录 replace 行为 |
| 实验统计 | 基础可用 | 返回事件计数和 like rate；高级指标待实现 |

## 推荐实施顺序

1. 先运行完整闭环：生成数据、导入、打开 Feed、记录行为、再次获取 Feed，确认偏好对结果生效。
2. 补齐行为语义与推荐日志，使每一次 Feed 都能关联 session、模式、探索度和展示商品。
3. 完成实验统计，优先产品浏览数、like rate、探索商品 like rate、风格跨度、换一件使用率。
4. 以固定数据和固定随机种子，比较 `baseline`、`balanced`、`explore` 三种模式。
5. 有足够实验数据后，再改进相似度和替换策略；不要在此之前接入向量模型。

## 模块实现契约

### 行为与偏好

文件：`backend/app/services/behavior_service.py`、`backend/app/services/preference_service.py`。

- 输入：`user_id`、`product_id`、`event_type`、`session_id`、可选 metadata。
- 输出：持久化的行为记录，以及更新后的 `UserPreference`。
- 实现：为 `replace`、`view`、`open_detail` 补充约定的权重；只更新商品的 `style_primary/style_secondary/category/color/fit`；每个权重限制在 -1 到 1。
- 验收：同一匿名用户喜欢 Workwear 后，`GET /users/{id}/preferences` 的 Workwear 权重增加，下一次 Feed 中相关商品占比提高。

### 推荐打分与多样性

文件：`backend/app/recommendation/scorer.py`、`diversity.py`、`engine.py`。

- 输入：用户偏好、候选商品、探索度（0–100）、请求数量。
- 输出：每个商品的总分、interest_score、novelty_score、推荐理由；按最终展示顺序返回。
- 实现：保持分数归一化到 0–1；探索度只经配置权重影响 interest/novelty/random；按 category/style/color 每 10 件最多 4 件、brand 最多 2 件重排。
- 验收：相同候选集下 baseline 的平均兴趣分高于 explore；explore 的平均新奇分和风格覆盖数高于 baseline；任何 Feed 不违反多样性上限。

### 换一件

文件：`backend/app/services/recommendation_service.py:replace`。

- `similar`：优先同 primary style，排除当前商品。
- `explore`：使用更高探索度，从相邻风格（建议以配置表定义）选取高 novelty 商品。
- `different`：排除当前 primary style，仍以用户兴趣分作为最低门槛。
- 每次调用必须写入一条 `replace` 行为，并返回与 Feed 相同的 `RecommendedProduct` 结构。
- 验收：三个 direction 不返回当前商品；similar 与 current 有相同风格；different 不同主风格。

### 实验指标

文件：`backend/app/api/experiments.py`。

先在 RecommendationLog 记录 `user_id/session_id/mode/exploration_level/product_ids`，并在首屏渲染时写 impression。随后实现：

| 指标 | 计算 |
| --- | --- |
| products_per_session | 一个 session 内 distinct product_id 数 |
| like_rate | like / impression |
| exploration_like_rate | novelty_score > 0.6 商品的 like / impression |
| unique_styles_per_session | 一个 session 内 distinct style_primary 数 |
| replace_usage_rate | 有 replace 的 session / 总 session |
| exploration_control_rate | 改变过探索度的匿名用户 / 总匿名用户 |

统计接口应支持 `from`、`to`、`mode`、`exploration_level` 过滤；没有数据时使用 0 或 `null`，避免除零异常。

### 搜索与商品来源

文件：`backend/app/repositories/product_repository.py`、`backend/app/integrations/`。

- 当前搜索必须保持 PostgreSQL `title/brand/style/category/color/description` 字段范围，不引入 Elasticsearch。
- 新增真实来源时只实现 `ProductProvider.search_products(query)` 与 `get_product(external_id)`；输出必须被映射为本项目 Product 字段。
- ProductService、RecommendationService 和前端禁止调用第三方 API SDK。
- 验收：替换 MockProvider 后，现有 `/products`、`/search`、`/recommendations/feed` 的响应结构不变。

## API 契约与手工验收

启动后，在 `/docs` 依序验证：

1. `GET /health` 返回 `status: ok`。
2. `GET /products?limit=1` 返回商品；`GET /products/{id}` 返回同一商品。
3. `GET /recommendations/feed?user_id=test-1&mode=balanced` 返回最多 20 件及 meta。
4. `POST /behaviors` 发送 like，然后读取 `/users/test-1/preferences`。
5. 再次获取 Feed，检查推荐理由和排序变化。
6. `POST /recommendations/replace` 分别传三种 direction。
7. `GET /experiments/stats` 返回合法 JSON。

## 测试建议

新增 `backend/tests/`，优先覆盖：模拟数据数量/标签覆盖、评分范围、多样性阈值、行为更新、替换方向和 API 状态码。测试数据库可用独立 PostgreSQL 容器；不要把测试依赖改为生产数据库。

前端可新增 Playwright 流程：首次访问创建匿名 ID、调整 Slider、喜欢商品、换一件、打开详情、进入实验页。任何 UI 测试都应 mock API 或使用隔离测试数据库。

## 配置与迁移规范

- 所有可调数值放在 `backend/app/config.py` 或环境变量，禁止散落硬编码。
- 每次修改 Model 后运行 `alembic revision --autogenerate -m "描述"`，审阅生成文件，再运行 `alembic upgrade head`。
- 不修改已执行的 migration；用新的 revision 演进 Schema。
- Mock 数据不是仓库依赖文件：运行 `python scripts/generate_products.py` 可完整重建。

## 完成 V0.1 的最终清单

- [ ] 新电脑按 README 使用本机或托管 PostgreSQL 启动后端、前端；Docker Desktop 不是前置条件。
- [ ] 连续浏览、喜欢/不喜欢/跳过/换一件会持久化行为并影响后续 Feed。
- [ ] 三种模式在同一数据上可比较，且输出实验指标。
- [ ] 5000 条数据覆盖 12 类、15 种风格、10+ 颜色、5+ 版型。
- [ ] 推荐、仓储、Provider 和 API 之间没有跨层数据库/供应商依赖。

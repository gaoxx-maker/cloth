# 后续工作（已实现 MVP 闭环之后的剩余项）

V0.1 骨架与核心闭环（Feed → 行为 → 偏好 → 再推荐 → 实验统计）已可运行。以下为真正留给后续迭代的工作，均非本阶段必须。

## 推荐算法增强

- `backend/app/recommendation/scorer.py:score_product`：当前 `similarity` 用兴趣分近似。待积累会话历史后，改为会话级相似度信号（同 Session 内浏览过的 style/category 相似度）。
- `backend/app/recommendation/diversity.py`：当前为贪心阈值重排，未来可替换为 MMR。
- `backend/app/repositories/product_repository.py:search_similar`：当前为属性启发式，未来换 pgvector 或独立向量服务。

## 真实商品来源接入

- `backend/app/integrations/taobao_provider.py`（及 jd/pdd）：当前为占位 `NotImplementedError`。接入时实现鉴权、限流与字段映射，输出必须映射为本项目 Product 字段，禁止让供应商字段流入服务层。接入后无需改动 ProductService / RecommendationService / 前端。

## 行为与实验

- `backend/app/api/experiments.py`：已实现 like_rate、探索商品 like_rate、每 session 浏览数、风格跨度、换一件使用率、探索度调节率。若需按 mode/exploration_level 过滤行为级指标，可将 impression 的 metadata 转成可查询列或单独统计表。
- 可新增 `backend/tests/`，覆盖数据量/标签覆盖、评分范围、多样性阈值、行为更新、替换方向与 API 状态码；前端可新增 Playwright 流程（mock API 或隔离测试库）。

## 环境与迁移

- 每次修改 Model 后运行 `alembic revision --autogenerate -m "描述"` 并审阅；不修改已执行的 migration。
- Mock 数据非仓库依赖：`python scripts/generate_products.py` 可完整重建；`python scripts/reset_database.py --yes` 清空业务表。

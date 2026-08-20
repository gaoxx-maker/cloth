# 架构

浏览器只通过 Next.js 调用 FastAPI REST API。API 将业务协调放在 `services/`，查询放在 `repositories/`；推荐模块只接收候选商品与偏好，不能访问数据库。`integrations/ProductProvider` 是未来真实商品来源的唯一入口。

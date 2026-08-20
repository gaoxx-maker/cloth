# 服装探索型推荐 Web MVP — 项目骨架开发需求 V0.1

## 1. 项目目标

本阶段**不是开发完整产品**，也不是上线商业版本。

当前唯一目标：

> 用最小成本建立一个可以运行的 Web MVP，验证“探索型服装推荐”是否能够实现，以及这种推荐方式是否比传统的高度相似推荐带来更强的浏览探索感。

核心验证问题：

> 用户是否愿意持续浏览“符合自己审美，但又有一定新奇度”的服装？

因此，本阶段只实现：

```text
商品数据库
+
用户行为记录
+
简单兴趣模型
+
探索型推荐算法
+
Web Feed
+
推荐实验参数
```

暂时不实现复杂商业能力。

---

# 2. 本阶段开发原则

开发方式采用：

> **先搭项目骨架，再逐模块补代码。**

AI / Agent 的任务不是一次性完成整个项目，而是：

1. 创建完整项目目录；
2. 创建必要文件；
3. 定义数据库；
4. 定义 API 接口；
5. 定义前后端数据结构；
6. 创建推荐系统接口；
7. 创建模拟商品数据生成器；
8. 创建页面基本结构；
9. 在需要开发的位置写明 TODO；
10. 告诉开发者每个 TODO 应该填入什么代码。

开发者后续逐模块实现具体逻辑。

代码应满足：

```text
模块低耦合
接口清晰
可以单独替换
方便未来接入真实商品 API
方便未来更换推荐算法
方便未来增加 AI
方便未来增加图片
方便未来增加 APP
```

---

# 3. MVP 范围

## 必须完成

### Web

实现网页版。

包含：

```text
首页 Feed
商品详情页
喜欢 / 不喜欢 / 跳过
换一件
探索度调节
简单搜索
实验数据页面
```

---

### 后端

实现：

```text
商品 API
推荐 API
行为记录 API
搜索 API
用户偏好 API
实验统计 API
```

---

### 数据库

本阶段不接淘宝、京东、拼多多等真实 API。

使用：

```text
PostgreSQL
```

模拟真实商品平台数据。

至少生成：

```text
3000 条商品数据
```

推荐：

```text
5000 条
```

如果生成成本较低，可以：

```text
10000 条
```

---

# 4. 当前技术栈

## 前端

```text
Next.js
React
TypeScript
```

---

## 后端

```text
Python
FastAPI
```

---

## 数据库

```text
PostgreSQL
```

ORM 推荐：

```text
SQLAlchemy
```

数据库迁移：

```text
Alembic
```

---

## 推荐算法

第一版只使用：

```text
规则
+
加权评分
+
受控随机
+
多样性控制
```

暂时不要：

```text
PyTorch
TensorFlow
Two-Tower
DeepFM
强化学习
复杂 Bandit
大模型推荐
```

---

# 5. 项目总体架构

```text
                       Browser
                          │
                          ▼
                    Next.js Web
                          │
                          ▼
                     FastAPI
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
      Product         Recommendation    Behavior
      Service            Service        Service
          │               │                │
          └───────────────┼────────────────┘
                          │
                          ▼
                     PostgreSQL
                          │
                          ▼
                   Mock Product Data
```

未来扩展：

```text
                       Product Service
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
          Mock DB          Taobao API      JD API
                                             
                              +
                              
                      Recommendation
                              │
           ┌──────────────────┼──────────────────┐
           ▼                  ▼                  ▼
       Rule Engine         ML Ranker          AI Ranker
```

因此当前代码禁止把数据库读取逻辑直接写死在推荐算法中。

必须通过 Service / Repository 抽象访问商品。

---

# 6. 推荐项目目录

```text
fashion-explorer/
│
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── frontend/
│   │
│   ├── package.json
│   ├── next.config.ts
│   ├── tsconfig.json
│   │
│   └── src/
│       │
│       ├── app/
│       │   ├── page.tsx
│       │   ├── product/
│       │   │   └── [id]/
│       │   │       └── page.tsx
│       │   ├── search/
│       │   │   └── page.tsx
│       │   └── experiment/
│       │       └── page.tsx
│       │
│       ├── components/
│       │   ├── ProductCard.tsx
│       │   ├── ProductFeed.tsx
│       │   ├── FeedbackButtons.tsx
│       │   ├── ExplorationSlider.tsx
│       │   └── SearchBar.tsx
│       │
│       ├── services/
│       │   ├── api.ts
│       │   ├── productApi.ts
│       │   ├── recommendationApi.ts
│       │   └── behaviorApi.ts
│       │
│       ├── types/
│       │   ├── product.ts
│       │   ├── user.ts
│       │   └── recommendation.ts
│       │
│       └── config/
│           └── constants.ts
│
├── backend/
│   │
│   ├── requirements.txt
│   ├── alembic.ini
│   │
│   └── app/
│       │
│       ├── main.py
│       │
│       ├── config.py
│       │
│       ├── database.py
│       │
│       ├── dependencies.py
│       │
│       ├── models/
│       │   ├── product.py
│       │   ├── user.py
│       │   ├── behavior.py
│       │   ├── recommendation.py
│       │   └── platform.py
│       │
│       ├── schemas/
│       │   ├── product.py
│       │   ├── behavior.py
│       │   ├── recommendation.py
│       │   └── user.py
│       │
│       ├── api/
│       │   ├── products.py
│       │   ├── recommendations.py
│       │   ├── behaviors.py
│       │   ├── search.py
│       │   └── experiments.py
│       │
│       ├── services/
│       │   ├── product_service.py
│       │   ├── recommendation_service.py
│       │   ├── behavior_service.py
│       │   ├── preference_service.py
│       │   └── search_service.py
│       │
│       ├── repositories/
│       │   ├── product_repository.py
│       │   ├── user_repository.py
│       │   └── behavior_repository.py
│       │
│       ├── recommendation/
│       │   ├── base.py
│       │   ├── scorer.py
│       │   ├── explorer.py
│       │   ├── diversity.py
│       │   └── engine.py
│       │
│       ├── integrations/
│       │   ├── base.py
│       │   ├── mock_provider.py
│       │   ├── taobao_provider.py
│       │   ├── jd_provider.py
│       │   └── pdd_provider.py
│       │
│       └── utils/
│           └── random_utils.py
│
├── scripts/
│   ├── generate_products.py
│   ├── seed_database.py
│   └── reset_database.py
│
├── data/
│   ├── styles.json
│   ├── brands.json
│   ├── categories.json
│   ├── colors.json
│   └── mock_products.json
│
└── docs/
    ├── architecture.md
    ├── database.md
    ├── recommendation.md
    ├── api.md
    ├── deployment.md
    └── TODO.md
```

---

# 7. 商品数据库设计

第一版不要建立过于复杂的 SPU/SKU 系统。

建立核心商品表：

```text
products
```

字段：

```text
id

title

description

brand

category

subcategory

price

original_price

color

fit

material

season

gender

style_primary

style_secondary

style_tags

novelty_score

popularity_score

quality_score

platform_id

external_product_id

product_url

created_at
```

因为当前不使用图片：

```text
image_url
```

字段可以保留，但：

```text
允许 NULL
```

---

# 8. 用文字替代图片

当前商品卡片不要展示真实商品图片。

用结构化文字描述商品。

例如：

```text
复古宽松工装夹克

品牌：Urban Archive

价格：¥329

颜色：军绿色

风格：
Vintage / Workwear / Japanese

版型：
宽松

材质：
棉

描述：
军绿色宽松短款工装夹克，
做旧水洗设计，
四口袋结构，
偏日系复古工装风。
```

前端可以使用一个简单的文字 Card：

```text
┌─────────────────────────┐

   复古宽松工装夹克

   Vintage · Workwear

   军绿色 / 宽松

   ¥329

   做旧水洗设计
   四口袋工装结构

   ♥ 喜欢
   × 不喜欢
   → 换一件

└─────────────────────────┘
```

这样可以大幅降低准备数据的成本。

---

# 9. 模拟商品数据要求

至少：

```text
3000
```

推荐：

```text
5000
```

商品。

不要手工创建。

必须创建：

```text
scripts/generate_products.py
```

自动组合生成。

---

# 10. 商品标签体系

第一版使用有限标签。

## Category

```text
T-Shirt
Shirt
Hoodie
Sweater
Jacket
Coat
Pants
Jeans
Cargo Pants
Shorts
Sneakers
Boots
```

---

## Style

建议：

```text
Streetwear
Vintage
Workwear
Minimal
Japanese
Korean
Y2K
Outdoor
Techwear
Preppy
Casual
Sports
Formal
Designer
Retro Sports
```

---

## Color

```text
Black
White
Gray
Navy
Blue
Brown
Khaki
Green
Army Green
Beige
Red
Burgundy
```

---

## Fit

```text
Slim
Regular
Relaxed
Oversized
Wide
Cropped
```

---

## Season

```text
Spring
Summer
Autumn
Winter
All Season
```

---

# 11. 模拟数据生成策略

不要完全随机组合。

否则可能出现：

```text
Formal + Cargo Pants + Running
```

之类不合理商品。

应该建立模板。

例如：

```python
STYLE_RULES = {
    "Workwear": {
        "categories": [...],
        "colors": [...],
        "fits": [...]
    },

    "Vintage": {
        ...
    }
}
```

然后：

```text
选择 style
↓
根据 style 选择 category
↓
选择合理 color
↓
选择 fit
↓
生成价格
↓
生成标题
↓
生成 description
↓
生成 novelty_score
```

---

# 12. 推荐系统核心设计

第一版最重要模块：

```text
backend/app/recommendation/
```

必须和 FastAPI、数据库逻辑解耦。

定义：

```python
class RecommendationEngine:
    def recommend(
        self,
        user_id,
        candidates,
        exploration_level,
        limit
    ):
        pass
```

以后无论换：

```text
规则算法
LightGBM
Two Tower
Bandit
LLM
```

都不需要修改 API。

---

# 13. 第一版推荐模型

推荐分数：

```text
score =

interest_score
+
similarity_score
+
novelty_score
+
quality_score
+
random_score
```

初始权重：

```text
interest        0.40
similarity      0.20
novelty         0.20
quality         0.10
random          0.10
```

注意：

这些只是实验参数。

必须写入：

```text
config
```

禁止直接散落在代码里。

例如：

```python
RECOMMENDATION_WEIGHTS = {
    "interest": 0.40,
    "similarity": 0.20,
    "novelty": 0.20,
    "quality": 0.10,
    "random": 0.10,
}
```

---

# 14. 用户兴趣模型

第一版不要使用 Embedding。

直接维护：

```text
用户喜欢哪些 style
用户喜欢哪些 color
用户喜欢哪些 category
用户喜欢哪些 fit
用户价格区间
```

例如：

```json
{
    "styles": {
        "Streetwear": 0.8,
        "Vintage": 0.7,
        "Workwear": 0.6,
        "Formal": 0.1
    },

    "colors": {
        "Black": 0.9,
        "Gray": 0.7,
        "Army Green": 0.6
    }
}
```

---

# 15. 用户行为

建立：

```text
user_behaviors
```

字段：

```text
id
user_id
product_id
event_type
session_id
metadata
created_at
```

event_type：

```text
impression
view
like
dislike
skip
replace
open_detail
search
favorite
```

---

# 16. 行为权重

初始实验值：

```text
like          +3
favorite      +4
open_detail   +1
view          +0.5
skip          -0.5
replace       -0.5
dislike       -3
```

用户点击：

```text
like
```

之后：

```text
style_primary
style_secondary
category
color
fit
```

对应偏好增加。

点击：

```text
dislike
```

则降低。

---

# 17. 探索度

Web 页面增加：

```text
探索度 Slider
```

范围：

```text
0 ---------------- 100
精准             探索
```

可以映射：

## 0

```text
interest 70%
novelty 10%
random 5%
```

## 50

```text
interest 45%
novelty 20%
random 10%
```

## 100

```text
interest 25%
novelty 35%
random 20%
```

核心目的：

> 验证用户是否喜欢主动控制推荐探索程度。

---

# 18. 多样性控制

不能只按照：

```python
sorted(products, key=score)
```

直接返回。

否则仍然可能出现：

```text
黑卫衣
黑卫衣
黑卫衣
黑卫衣
```

需要增加简单规则。

例如连续 10 个商品：

```text
同 category <= 4
同 primary_style <= 4
同 brand <= 2
同 color <= 4
```

创建：

```text
diversity.py
```

专门负责重新排序。

未来这里可以替换成：

```text
MMR
```

---

# 19. “换一件”功能

这是 MVP 的重点。

API：

```text
POST /recommendations/replace
```

输入：

```json
{
    "user_id": 1,
    "product_id": 125,
    "direction": "similar"
}
```

direction：

```text
similar
explore
different
```

---

## similar

寻找：

```text
同风格
+
不同商品
```

---

## explore

寻找：

```text
相邻风格
+
较高 novelty
```

---

## different

寻找：

```text
明显不同风格
+
仍具有一定兴趣概率
```

这是未来“兴趣扩散”的基础接口。

---

# 20. API 模块

至少定义：

```text
GET /products
GET /products/{id}

GET /recommendations/feed

POST /recommendations/replace

POST /behaviors

GET /search

GET /users/{id}/preferences

GET /experiments/stats
```

---

# 21. API 返回结构

Feed：

```json
{
    "items": [],
    "meta": {
        "exploration_level": 50,
        "algorithm": "rule_v1"
    }
}
```

每个商品：

```json
{
    "id": 125,

    "title": "Vintage Workwear Jacket",

    "price": 329,

    "brand": "Urban Archive",

    "category": "Jacket",

    "styles": [
        "Vintage",
        "Workwear"
    ],

    "color": "Army Green",

    "fit": "Oversized",

    "description": "...",

    "recommendation": {
        "score": 0.72,
        "interest_score": 0.68,
        "novelty_score": 0.81,
        "reason": [
            "你喜欢复古风",
            "与你最近浏览的工装风格相关",
            "这件商品具有较高探索度"
        ]
    }
}
```

---

# 22. 首页

第一版首页尽量简单。

```text
----------------------------------

Fashion Explorer

精准 ←─────●─────→ 探索

----------------------------------

Vintage Workwear Jacket

Vintage / Workwear

Army Green
Oversized

¥329

做旧水洗工装夹克，
偏日系复古风格。

为什么推荐：
你喜欢 Vintage
+
这件商品具有较高新奇度

[喜欢]

[不喜欢]

[换一件]

[查看详情]

----------------------------------
```

不要花大量时间做 UI。

当前验证重点是：

```text
推荐体验
```

而不是视觉设计。

---

# 23. 搜索

第一版只使用 PostgreSQL 查询。

支持：

```text
title
brand
style
category
color
description
```

不要使用：

```text
Elasticsearch
向量搜索
LLM
```

但是必须保留：

```text
SearchService
```

以后可以把 PostgreSQL Search 换成 Elasticsearch。

---

# 24. 商户 API 模块必须保留

虽然当前不用真实平台 API，但是必须建立：

```text
integrations/
```

统一接口：

```python
class ProductProvider:

    def search_products(self, query):
        raise NotImplementedError

    def get_product(self, external_id):
        raise NotImplementedError
```

当前：

```text
MockProductProvider
```

从数据库读取。

未来：

```text
TaobaoProvider
JDProvider
PDDProvider
DewuProvider
```

接真实平台。

这样未来无需修改：

```text
RecommendationService
ProductService
Frontend
```

---

# 25. 数据来源抽象

ProductService 不允许：

```text
直接依赖淘宝 API
```

应该：

```text
ProductService
        │
        ▼
ProductProvider
        │
 ┌──────┼────────┐
 ▼      ▼        ▼
Mock    JD      Taobao
DB      API       API
```

本阶段：

```text
ProductProvider = MockProductProvider
```

---

# 26. 为未来功能预留模块

当前只创建接口和目录，不实现。

---

## 图片理解

预留：

```text
ai/
    vision/
```

以后：

```text
CLIP
SigLIP
VLM
```

---

## Embedding

预留：

```text
embedding/
```

以后：

```text
product_embedding
user_embedding
style_embedding
```

---

## Agent

预留：

```text
agent/
```

未来：

```text
ShoppingAgent
SearchTool
RecommendationTool
PriceTool
```

---

## 向量搜索

Repository 层提前允许：

```text
search_similar()
```

但第一版：

```text
NotImplemented
```

---

## APP

所有功能通过 REST API 提供。

因此未来：

```text
Android APP
        │
        ▼
     FastAPI
```

可以直接复用后端。

---

# 27. 实验数据

这是 MVP 很重要但很容易被忽略的部分。

记录：

```text
Feed impression
like
dislike
skip
replace
detail click
session length
products viewed
style transitions
```

---

# 28. 当前验证指标

重点关注：

## 每次 Session 浏览商品数量

```text
products_per_session
```

---

## Like Rate

```text
likes / impressions
```

---

## 探索商品 Like Rate

定义：

```text
novelty_score > 0.6
```

统计：

```text
exploration_like_rate
```

这是非常重要的指标。

---

## 风格跨度

例如：

```text
Streetwear
↓
Vintage
↓
Workwear
↓
Japanese
```

统计：

```text
unique_styles_per_session
```

---

## Replace 使用率

```text
replace_count / sessions
```

---

## 探索度调节率

```text
users_changed_exploration_level
```

---

# 29. MVP 成功标准

不是看：

```text
购买数量
GMV
广告收入
```

而是看：

> 用户是否愿意探索。

例如初步观察：

```text
平均浏览商品数量
探索商品 Like Rate
独立风格浏览数量
换一件使用率
Session 时长
重复访问率
```

如果：

```text
用户大量浏览
+
经常喜欢不同风格
+
会主动提高探索度
+
会频繁使用“换一件”
```

说明产品方向值得继续测试。

---

# 30. 当前不要做的功能

第一版明确禁止投入大量时间开发：

```text
淘宝 API
京东 API
拼多多 API

真实支付

真实购买

复杂 SKU

图片抓取

图片存储

CLIP

SigLIP

VLM

YOLO

向量数据库

Elasticsearch

Redis

Kafka

微服务

Kubernetes

机器学习训练

深度推荐模型

AI Agent

Android APP

iOS APP

复杂登录

短信验证码

第三方 OAuth
```

这些全部等核心假设验证之后再做。

---

# 31. 第一版用户系统

为了最快开发：

不要实现完整注册系统。

可以：

```text
自动创建匿名用户
```

例如：

```text
localStorage:
user_id = uuid
```

第一次访问：

```text
创建匿名用户
```

之后记录行为即可。

未来再增加：

```text
登录
注册
OAuth
```

---

# 32. Docker

开发环境建议提供：

```text
docker-compose.yml
```

只运行：

```text
PostgreSQL
```

前端后端开发阶段可以本地运行。

例如：

```text
PostgreSQL → Docker

FastAPI → localhost:8000

Next.js → localhost:3000
```

---

# 33. 部署要求

AI / Agent：

> 不负责实际部署。

只需要创建：

```text
docs/deployment.md
```

说明开发者未来如何部署。

至少解释：

```text
1. 如何部署 PostgreSQL
2. 如何设置 DATABASE_URL
3. 如何启动 FastAPI
4. 如何部署 Next.js
5. 如何设置环境变量
6. 如何配置 CORS
7. 如何配置生产 API 地址
```

可以推荐未来部署方式，例如：

```text
Frontend
→ Vercel

Backend
→ Render / Railway / 云服务器

Database
→ PostgreSQL 云数据库
```

但：

> 不执行真实部署操作。

---

# 34. 环境变量

创建：

```text
.env.example
```

例如：

```text
DATABASE_URL=

NEXT_PUBLIC_API_URL=

ENVIRONMENT=development

RECOMMENDATION_ALGORITHM=rule_v1

DEFAULT_EXPLORATION_LEVEL=50
```

未来：

```text
TAOBAO_API_KEY=
JD_API_KEY=
PDD_API_KEY=
```

暂时留空。

---

# 35. Agent 编码规则

AI Agent 必须遵守：

### 1

不要一次性实现整个项目。

优先完成：

```text
目录
接口
Schema
数据结构
TODO
README
```

---

### 2

重要文件必须包含：

```text
TODO
```

并说明：

```text
这里需要开发者实现什么。
```

---

### 3

每个 TODO 应包含：

```text
输入是什么
输出是什么
应该实现什么逻辑
涉及哪些数据
推荐实现方式
```

例如：

```python
def calculate_interest_score(user, product):
    """
    TODO:

    根据用户 preference 和商品属性计算兴趣分数。

    输入：
        user preference
        product

    输出：
        float 0~1

    第一版建议比较：
        style
        category
        color
        fit

    推荐权重：
        style = 0.4
        category = 0.25
        color = 0.2
        fit = 0.15
    """
    raise NotImplementedError
```

---

# 36. 不允许出现

不要生成大量类似：

```python
pass
```

却没有解释。

所有未实现代码必须说明：

```text
为什么存在
未来负责什么
现在应该怎么补
```

---

# 37. 开发任务顺序

严格按照以下顺序。

## Phase 1：项目骨架

创建：

```text
frontend
backend
scripts
data
docs
```

并保证：

```text
Next.js 可以启动
FastAPI 可以启动
```

---

## Phase 2：数据库

创建：

```text
Product
User
UserBehavior
RecommendationLog
Platform
UserPreference
```

完成 Alembic。

---

## Phase 3：模拟数据

实现：

```text
generate_products.py
```

生成：

```text
5000 商品
```

然后：

```text
seed_database.py
```

写入 PostgreSQL。

---

## Phase 4：商品 API

完成：

```text
/products
/products/{id}
/search
```

---

## Phase 5：行为系统

完成：

```text
like
dislike
skip
replace
view
```

记录。

---

## Phase 6：推荐框架

先创建：

```text
RecommendationEngine
Scorer
Explorer
DiversityReranker
```

不需要最优算法。

---

## Phase 7：首页

实现基本 Feed。

---

## Phase 8：探索算法

开始开发：

```text
Interest Score
Novelty Score
Random Exploration
Diversity
```

---

## Phase 9：实验统计

增加：

```text
experiments/stats
```

---

## Phase 10：测试

比较：

```text
传统模式
VS
探索模式
```

---

# 38. 推荐实验设计

系统至少提供三种推荐模式。

## baseline

```text
几乎完全根据兴趣排序
```

---

## balanced

```text
兴趣
+
一定探索
```

---

## explore

```text
明显提高 novelty 和 diversity
```

例如：

```text
?mode=baseline
```

```text
?mode=balanced
```

```text
?mode=explore
```

方便直接比较。

---

# 39. 数据量

开发环境默认：

```text
5000 商品
```

最低必须：

```text
>= 3000
```

数据必须覆盖至少：

```text
12 categories

15 styles

10+ colors

5+ fits

多个价格区间
```

这样推荐算法才有足够的探索空间。

---

# 40. 项目最终运行流程

```text
git clone
↓
创建 .env
↓
docker compose up postgres
↓
运行 migration
↓
python scripts/generate_products.py
↓
python scripts/seed_database.py
↓
启动 FastAPI
↓
启动 Next.js
↓
打开 localhost:3000
↓
生成匿名用户
↓
浏览 Feed
↓
喜欢 / 不喜欢 / 换一件
↓
更新用户偏好
↓
下一批推荐发生变化
↓
查看实验指标
```

---

# 41. 当前 MVP 核心闭环

最终必须能够跑通：

```text
用户进入网站
        ↓
系统推荐 20 件商品
        ↓
用户浏览
        ↓
喜欢 / 不喜欢 / 跳过
        ↓
记录行为
        ↓
更新兴趣画像
        ↓
下一次推荐
        ↓
部分符合兴趣
+
部分相似
+
部分新奇
        ↓
继续浏览
```

如果这个闭环可以运行：

> V0.1 即视为完成。

---

# 42. 验收标准

项目骨架阶段完成标准：

- [ ] frontend 可以启动
- [ ] backend 可以启动
- [ ] PostgreSQL 可以连接
- [ ] Alembic migration 可以运行
- [ ] 数据库 Schema 完成
- [ ] 可以生成至少 3000 条商品
- [ ] 推荐生成 5000 条商品
- [ ] ProductProvider 抽象完成
- [ ] MockProvider 完成
- [ ] 淘宝/JD 等 Provider 已预留接口
- [ ] RecommendationEngine 接口完成
- [ ] 推荐算法各子模块位置明确
- [ ] 用户行为 Schema 完成
- [ ] Feed API 接口定义完成
- [ ] 前端页面骨架完成
- [ ] 每个未完成模块都有明确 TODO
- [ ] docs 中解释完整架构
- [ ] docs/deployment.md 说明未来如何部署
- [ ] README 给出完整本地运行方式

---

# 43. AI Agent 当前任务

现在请不要替我完成整个产品。

你的任务是：

> **搭建一套可以继续开发的工程骨架。**

你需要：

1. 创建上述项目目录；
2. 创建基本配置；
3. 创建数据库模型；
4. 创建 API Router；
5. 创建 Service；
6. 创建 Repository；
7. 创建 ProductProvider 抽象；
8. 创建推荐算法抽象；
9. 创建模拟数据生成框架；
10. 创建前端页面骨架；
11. 创建前端 API Service；
12. 创建 TypeScript 类型；
13. 创建 README；
14. 创建 architecture.md；
15. 创建 database.md；
16. 创建 recommendation.md；
17. 创建 deployment.md；
18. 创建 TODO.md。

对于尚未实现的功能：

必须告诉我：

```text
文件路径
↓
需要修改的函数
↓
需要输入什么
↓
需要输出什么
↓
实现逻辑
↓
建议代码结构
```

不要只告诉我：

> “这里以后实现推荐算法。”

必须告诉我：

> “打开 backend/app/recommendation/scorer.py，实现 calculate_interest_score()，读取 UserPreference 中 style/category/color/fit 权重，与 Product 对应字段进行匹配，最后归一化为 0~1。”

---

# 44. 当前 MVP 的真正目标

不要为了工程完整性增加功能。

这个项目现在只回答一个问题：

> **探索型推荐是否真的能让用户看到更多不同类型的衣服，同时又不会因为过于随机而失去兴趣？**

所有不能帮助回答这个问题的功能：

> 暂缓开发。

项目必须满足 reproducible development environment：

任何新的 Windows 电脑 clone GitHub 仓库后，
在安装 Git、Python、Node.js 和 Docker Desktop 的前提下，
不依赖原开发电脑的任何本地文件，
按照 README.md 即可完整启动前端、后端、PostgreSQL，
并重新生成全部模拟商品数据。

禁止：
1. 使用开发者电脑的绝对路径；
2. 依赖未提交的本地文件；
3. 将密码/API Key 写死在源码；
4. 要求手动创建数据库表；
5. 要求手动插入测试商品数据。
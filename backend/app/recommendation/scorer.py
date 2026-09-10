"""规则评分器：把用户偏好、商品属性与探索度换算成 0~1 的子分数与总分。

这是第一版推荐模型的核心，仅使用规则 + 加权评分 + 受控随机，不引入机器学习。
后续替换为 LightGBM / Two-Tower / Bandit 时，只需保持 `score_product` 的输入输出契约不变。
"""
import random

from app.config import EXPLORATION_INTERP, RECOMMENDATION_WEIGHTS, SEASONALITY_WEIGHT

# 兴趣画像各维度的权重：把 style/category/color/fit 的偏好匹配合成单一兴趣分。
INTEREST_DIMENSION_WEIGHTS = {"style": 0.40, "category": 0.25, "color": 0.20, "fit": 0.15}


def _normalize_match(value: float) -> float:
    """把 [-1, 1] 的偏好匹配值归一化到 [0, 1]：-1 -> 0，0 -> 0.5，1 -> 1。"""
    return max(0.0, min(1.0, (value + 1.0) / 2.0))


def calculate_interest_score(preference, product) -> float:
    """比较用户偏好与商品属性，输出 0~1 的兴趣分。

    偏好来自 UserPreference 的 styles/categories/colors/fits 四个 JSON 字段，
    每个值为 -1~1（缺失维度按 0 中性处理）。加权求和后归一化到 0~1。
    """
    weighted = (
        float((preference.styles or {}).get(product.style_primary, 0.0)) * INTEREST_DIMENSION_WEIGHTS["style"]
        + float((preference.categories or {}).get(product.category, 0.0)) * INTEREST_DIMENSION_WEIGHTS["category"]
        + float((preference.colors or {}).get(product.color, 0.0)) * INTEREST_DIMENSION_WEIGHTS["color"]
        + float((preference.fits or {}).get(product.fit, 0.0)) * INTEREST_DIMENSION_WEIGHTS["fit"]
    )
    return _normalize_match(weighted)


def _weights_for_exploration(exploration_level: int) -> dict:
    """按探索度 0~100 插值各分量的权重并归一化，保证权重之和恒为 1。"""
    t = max(0, min(100, exploration_level)) / 100.0
    weights = dict(RECOMMENDATION_WEIGHTS)
    for key, (low, high) in EXPLORATION_INTERP.items():
        weights[key] = low + (high - low) * t
    total = sum(weights.values())
    return {k: v / total for k, v in weights.items()}


def _season_score(product_season: str | None, current_season: str) -> float:
    """当季和四季款为 1，其余季节为 0；由最终加权而非硬过滤处理。"""
    return 1.0 if product_season in {current_season, "All Season"} else 0.0


def score_product(preference, product, exploration_level: int, current_season: str) -> dict:
    """计算单个商品的子分数与总分。

    similarity 暂用兴趣分近似（同一风格大概率也相似），待累积会话历史后替换为
    真正的会话相似度信号。random_score 提供受控随机，让每批推荐不完全一致。
    """
    weights = _weights_for_exploration(exploration_level)
    interest = calculate_interest_score(preference, product)
    novelty = float(product.novelty_score)
    quality = float(product.quality_score)
    random_score = random.random()
    season = _season_score(product.season, current_season)

    base_score = (
        weights["interest"] * interest
        + weights["similarity"] * interest
        + weights["novelty"] * novelty
        + weights["quality"] * quality
        + weights["random"] * random_score
    )
    score = (1 - SEASONALITY_WEIGHT) * base_score + SEASONALITY_WEIGHT * season
    return {
        "score": score,
        "interest_score": interest,
        "novelty_score": novelty,
        "season_score": season,
    }

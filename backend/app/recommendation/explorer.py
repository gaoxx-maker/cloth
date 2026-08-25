"""推荐理由生成：把评分结果转成用户可读的一句话，解释“为什么推荐这件”。"""


def reasons(product, interest_score: float, exploration_level: int, current_season: str, preference=None) -> list[str]:
    result = []

    # 只有当用户确实对某个维度有正向偏好时，才给出“你喜欢 X”的理由；
    # 避免中性（无历史）用户看到误导性的“与你偏好相关”。
    if preference is not None:
        styles = preference.styles or {}
        categories = preference.categories or {}
        colors = preference.colors or {}
        fits = preference.fits or {}

        if styles.get(product.style_primary, 0) > 0:
            result.append(f"你喜欢 {product.style_primary} 风格")
        elif categories.get(product.category, 0) > 0:
            result.append(f"你喜欢 {product.category} 品类")
        elif colors.get(product.color, 0) > 0:
            result.append(f"你喜欢 {product.color} 色系")
        elif fits.get(product.fit, 0) > 0:
            result.append(f"你喜欢 {product.fit} 版型")

    if exploration_level >= 50 and product.novelty_score > 0.6:
        result.append("这件商品具有较高探索度")

    if product.season in {current_season, "All Season"}:
        result.append("适合当前季节穿着")

    return result or ["为你保留的一件新风格单品"]

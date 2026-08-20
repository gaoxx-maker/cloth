"""多样性重排：贪心挑选，保证 Feed 中同类目/风格/颜色不过度集中。"""
from app.config import DIVERSITY_LIMITS


def rerank_diverse(scored: list[tuple], limit: int) -> list[tuple]:
    """按总分从高到低贪心挑选，同时满足多样性上限。

    每个候选商品若其 category/style_primary/color/brand 已出现次数未达上限，
    则入选并累加计数；否则跳过。未来可替换为 MMR 等更平滑的多样性算法。
    """
    result: list[tuple] = []
    counts: dict[tuple, int] = {}

    # 键 -> (类别标签, 上限)：category/style/color <= 4、brand <= 2。
    constraints = [
        ("category", "category", DIVERSITY_LIMITS["category"]),
        ("style", "style_primary", DIVERSITY_LIMITS["style"]),
        ("color", "color", DIVERSITY_LIMITS["color"]),
        ("brand", "brand", DIVERSITY_LIMITS["brand"]),
    ]

    for product, score in sorted(scored, key=lambda item: item[1]["score"], reverse=True):
        keys = [(kind, getattr(product, attr)) for kind, attr, _ in constraints]
        maximums = {kind: maximum for kind, _, maximum in constraints}
        if all(counts.get(key, 0) < maximums[kind] for kind, key in keys):
            result.append((product, score))
            for key in keys:
                counts[key] = counts.get(key, 0) + 1
        if len(result) == limit:
            break
    return result

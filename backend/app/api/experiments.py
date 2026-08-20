"""实验统计：把行为 + 推荐日志汇总成可读的探索指标。"""
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.behavior import UserBehavior
from app.models.product import Product
from app.models.recommendation import RecommendationLog

router = APIRouter(prefix="/experiments", tags=["experiments"])

# novelty_score 超过该阈值的商品视为「探索型商品」。
NOVELTY_THRESHOLD = 0.6


def _div(numerator: int, denominator: int) -> float | None:
    """安全除法：分母为 0 时返回 None，避免除零异常。"""
    return round(numerator / denominator, 4) if denominator else None


def _avg(values: list[int]) -> float | None:
    return round(sum(values) / len(values), 2) if values else None


@router.get("/stats")
def stats(
    db: Session = Depends(get_db),
    start: datetime | None = Query(None, alias="from"),
    end: datetime | None = Query(None, alias="to"),
    mode: str | None = None,
    exploration_level: int | None = None,
):
    """汇总探索实验的核心指标，支持时间范围 / 模式 / 探索度过滤。"""
    behavior = UserBehavior

    # 1) 各事件类型的计数
    event_q = select(behavior.event_type, func.count()).group_by(behavior.event_type)
    if start:
        event_q = event_q.where(behavior.created_at >= start)
    if end:
        event_q = event_q.where(behavior.created_at <= end)
    events = dict(db.execute(event_q).all())

    # 2) 行为 + 商品，用于 novelty 与风格跨度指标
    joined_q = select(behavior, Product).join(Product, Product.id == behavior.product_id)
    if start:
        joined_q = joined_q.where(behavior.created_at >= start)
    if end:
        joined_q = joined_q.where(behavior.created_at <= end)
    rows = db.execute(joined_q).all()

    explore_impressions = 0
    explore_likes = 0
    sessions: dict[str, dict] = {}

    for behavior, product in rows:
        if product is None:
            continue

        is_explore = (product.novelty_score or 0) > NOVELTY_THRESHOLD
        if behavior.event_type == "impression" and is_explore:
            explore_impressions += 1
        elif behavior.event_type == "like" and is_explore:
            explore_likes += 1

        if behavior.session_id:
            sess = sessions.setdefault(
                behavior.session_id,
                {"products": set(), "styles": set(), "has_replace": False},
            )
            sess["products"].add(product.id)
            sess["styles"].add(product.style_primary)
            if behavior.event_type == "replace":
                sess["has_replace"] = True

    total_sessions = len(sessions)
    sessions_with_replace = sum(1 for s in sessions.values() if s["has_replace"])

    # 3) 推荐日志 → 探索度调节率（同一用户出现多个探索度值即视为调整过 Slider）
    log_q = select(RecommendationLog)
    if start:
        log_q = log_q.where(RecommendationLog.created_at >= start)
    if end:
        log_q = log_q.where(RecommendationLog.created_at <= end)
    if mode:
        log_q = log_q.where(RecommendationLog.mode == mode)
    if exploration_level is not None:
        log_q = log_q.where(RecommendationLog.exploration_level == exploration_level)
    logs = db.execute(log_q).scalars().all()

    levels_by_user: dict[str, set[int]] = {}
    for log in logs:
        levels_by_user.setdefault(log.user_id, set()).add(log.exploration_level)
    total_users = len(levels_by_user)
    users_changed = sum(1 for levels in levels_by_user.values() if len(levels) > 1)

    return {
        "events": events,
        "like_rate": _div(events.get("like", 0), events.get("impression", 0)),
        "exploration_like_rate": _div(explore_likes, explore_impressions),
        "products_per_session": _avg([len(s["products"]) for s in sessions.values()]),
        "unique_styles_per_session": _avg([len(s["styles"]) for s in sessions.values()]),
        "replace_usage_rate": _div(sessions_with_replace, total_sessions),
        "exploration_control_rate": _div(users_changed, total_users),
        "replace_count": events.get("replace", 0),
        "total_sessions": total_sessions,
        "total_users": total_users,
    }

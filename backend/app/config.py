from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# 项目根目录（backend/app/config.py 向上两级），.env 一律按此绝对路径解析，
# 保证无论从 backend/ 还是项目根目录运行脚本/服务都能读到同一份配置。
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    """运行时配置，一律通过环境变量 / .env 注入，禁止在源码中散落可调数值。"""

    model_config = SettingsConfigDict(env_file=str(ENV_FILE), extra="ignore")

    database_url: str = "postgresql+psycopg://fashion_explorer:fashion_explorer@localhost:5432/fashion_explorer"
    environment: str = "development"
    recommendation_algorithm: str = "rule_v1"
    default_exploration_level: int = 50
    cors_origins: list[str] = ["http://localhost:3000"]


# 推荐总分各分量的基础权重（实验参数）。探索度会在此基础上插值调整 interest/novelty/random。
RECOMMENDATION_WEIGHTS = {
    "interest": 0.40,
    "similarity": 0.20,
    "novelty": 0.20,
    "quality": 0.10,
    "random": 0.10,
}

# 探索度 0 -> 1 时 interest / novelty / random 权重的插值端点 (起点, 终点)。
# 0 = 精准（interest 70% / novelty 10% / random 5%），1 = 探索（interest 25% / novelty 35% / random 20%）。
EXPLORATION_INTERP = {
    "interest": (0.70, 0.25),
    "novelty": (0.10, 0.35),
    "random": (0.05, 0.20),
}

# 行为事件对兴趣画像的权重增量（原始幅度）。写入前会归一化并裁剪到 [-1, 1]。
BEHAVIOR_WEIGHTS = {
    "like": 3,
    "favorite": 4,
    "open_detail": 1,
    "view": 0.5,
    "skip": -0.5,
    "replace": -0.5,
    "dislike": -3,
}

# 相邻风格表：换一件「探索」方向从当前主风格扩散到相邻风格。
STYLE_ADJACENCY = {
    "Streetwear": ["Japanese", "Y2K", "Casual", "Retro Sports"],
    "Vintage": ["Workwear", "Japanese", "Casual"],
    "Workwear": ["Vintage", "Outdoor", "Japanese", "Techwear"],
    "Minimal": ["Korean", "Formal", "Preppy"],
    "Japanese": ["Minimal", "Vintage", "Streetwear", "Outdoor"],
    "Korean": ["Minimal", "Preppy", "Casual"],
    "Y2K": ["Streetwear", "Retro Sports", "Casual"],
    "Outdoor": ["Workwear", "Techwear", "Sports"],
    "Techwear": ["Workwear", "Outdoor", "Streetwear"],
    "Preppy": ["Minimal", "Korean", "Formal"],
    "Casual": ["Minimal", "Streetwear", "Korean"],
    "Sports": ["Outdoor", "Retro Sports", "Casual"],
    "Formal": ["Minimal", "Preppy"],
    "Designer": ["Formal", "Minimal"],
    "Retro Sports": ["Streetwear", "Sports", "Y2K"],
}

# 多样性上限：Feed 中同类目/风格/颜色最多 4 件、同品牌最多 2 件（见 diversity.py）。
DIVERSITY_LIMITS = {"category": 4, "style": 4, "color": 4, "brand": 2}


@lru_cache
def get_settings() -> Settings:
    return Settings()

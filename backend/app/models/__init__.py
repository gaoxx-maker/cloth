from app.models.platform import Platform
from app.models.product import Product
from app.models.user import User, UserPreference
from app.models.account import Account
from app.models.behavior import UserBehavior
from app.models.recommendation import RecommendationLog

__all__ = ["Platform", "Product", "User", "UserPreference", "Account", "UserBehavior", "RecommendationLog"]

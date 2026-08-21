from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import behaviors, experiments, products, recommendations, search, users
from app.config import get_settings

settings = get_settings()

app = FastAPI(title="Fashion Explorer API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (
    products.router,
    recommendations.router,
    behaviors.router,
    search.router,
    experiments.router,
    users.router,
):
    app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.environment}

from fastapi import APIRouter

from app.api.routes import categories, login, organizations, private, products, roles, users, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(
    organizations.router, prefix="/organizations", tags=["organizations"]
)
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(users.router)
api_router.include_router(
    categories.router, prefix="/categories", tags=["categories"]
)
api_router.include_router(
    products.router, prefix="/products", tags=["products"]
)
api_router.include_router(utils.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)

from fastapi import APIRouter

from presentation.users.routers import user_router

router = APIRouter(prefix="/api/v1")

router.include_router(user_router, prefix="/users", tags=["Users"])

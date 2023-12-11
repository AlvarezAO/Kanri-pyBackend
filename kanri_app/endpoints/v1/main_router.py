# app/api/api.py

from fastapi import APIRouter
from kanri_app.modules.users.endpoints import get_all_users, get_user, post_user, update_user
from kanri_app.modules.auth.endpoints import get_token


router = APIRouter()


router.include_router(get_token.router, tags=["Login"])
router.include_router(get_user.router, tags=["Users"])
router.include_router(get_all_users.router, tags=["Users"])
router.include_router(post_user.router, tags=["Users"])
router.include_router(update_user.router, tags=["Users"])

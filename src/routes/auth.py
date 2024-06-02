from fastapi import APIRouter

from src.controllers.auth import AuthController
from src.models.user import Token

router = APIRouter(prefix="/auth", tags=["auth"])

router.add_api_route(
    "/login", AuthController.login, methods=["POST"], response_model=Token
)

router.add_api_route(
    "/register", AuthController.register, methods=["POST"], response_model=Token
)

router.add_api_route(
    "/google-url",
    AuthController.google_auth_url,
    methods=["GET"],
    response_model=str,
)

router.add_api_route(
    "/google-callback",
    AuthController.google_auth_callback,
    methods=["GET"],
    response_model=Token,
)

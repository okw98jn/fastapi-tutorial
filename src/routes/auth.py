from fastapi import APIRouter

from src.controllers.auth import AuthController

router = APIRouter(prefix="/auth", tags=["auth"])

router.add_api_route("/login", AuthController.login, methods=["POST"])

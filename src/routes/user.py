from fastapi import APIRouter

from src.controllers.user import UserController

router = APIRouter(prefix="/users", tags=["users"])

router.add_api_route("/", UserController.index, methods=["GET"])

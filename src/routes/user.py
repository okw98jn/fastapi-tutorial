from fastapi import APIRouter

from src.controllers.user import UserController
from src.models.user import UserPublic

router = APIRouter(prefix="/users", tags=["users"])

router.add_api_route(
    "/", UserController.index, methods=["GET"], response_model=list[UserPublic]
)
router.add_api_route(
    "/{user_id}", UserController.show, methods=["GET"], response_model=UserPublic
)
router.add_api_route(
    "/", UserController.create, methods=["POST"], response_model=UserPublic
)
router.add_api_route(
    "/{user_id}", UserController.update, methods=["PUT"], response_model=UserPublic
)
router.add_api_route(
    "/{user_id}", UserController.delete, methods=["DELETE"], response_model=dict
)

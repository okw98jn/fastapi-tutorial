from fastapi import APIRouter

from src.controllers.user import UserController

router = APIRouter(prefix="/users", tags=["users"])

router.add_api_route("/", UserController.index, methods=["GET"])
router.add_api_route("/{user_id}", UserController.show, methods=["GET"])
router.add_api_route("/", UserController.create, methods=["POST"])
router.add_api_route("/{user_id}", UserController.update, methods=["PUT"])
router.add_api_route("/{user_id}", UserController.delete, methods=["DELETE"])

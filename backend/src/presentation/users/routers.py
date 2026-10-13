# TODO: separate the control plane from the data plane, and the api plane from the business logic plane

from fastapi import APIRouter

from presentation.users.schemas import CreateUserRequest

user_router = APIRouter()

@user_router.post("/")
def create_user(request: CreateUserRequest):
    return request

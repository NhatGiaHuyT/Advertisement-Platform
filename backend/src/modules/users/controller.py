from .schemas import CreateUserRequest, CreateUserResponse
from ...application.service.users import UserService, CreateUserInput, CreateUserDTO


class CreateUsersController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def handle(self, request: CreateUserRequest):
        input = CreateUserInput(
            first_name=request.first_name,
            last_name=request.last_name,
            username=request.username,
            email=request.email,
            password=request.password
        )

        result = await self.user_service.create_user(input)

        return CreateUserDTO(
            first_name=result.first_name,
            last_name=result.last_name,
            username=result.username,
            email=result.email,
        )
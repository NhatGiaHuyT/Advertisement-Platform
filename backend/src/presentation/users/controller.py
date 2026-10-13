from application.users.create_user import CreateUserCommand, ICreateUser
from presentation.users.schemas import CreateUserRequest, CreateUserResponse


class CreateUserController:
    def __init__(self, create_user: ICreateUser):
        self.create_user = create_user

    async def handle(self, request: CreateUserRequest):
        command = CreateUserCommand(
            first_name=request.first_name,
            last_name=request.last_name,
            username=request.username,
            email=request.email,
            created_at=request.created_at,
            password=request.password,
        )

        result = await self.create_user.execute(command)

        return CreateUserResponse(
            first_name=result.first_name,
            last_name=result.last_name,
            username=result.username,
            email=result.email,
        )

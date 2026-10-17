from fastapi import HTTPException, status

from application.users.create_user import CreateUserCommand, ICreateUser
from presentation.users.schemas import CreateUserRequest, CreateUserResponse


class CreateUserController:
    def __init__(self, create_user: ICreateUser):
        self.create_user = create_user

    async def handle(self, request: CreateUserRequest):
        try:
            command = CreateUserCommand(
                organization_id=request.organization_id,
                first_name=request.first_name,
                last_name=request.last_name,
                username=request.username,
                email=request.email,
                created_at=request.created_at,
                password=request.password,
            )

            output = await self.create_user.execute(command)

            return CreateUserResponse(
                id=output.id,
                first_name=output.first_name,
                last_name=output.last_name,
                username=output.username,
                email=output.email,
                created_at=output.created_at,
                user_status=output.user_status,
            )
        except ValueError as err:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)) from err

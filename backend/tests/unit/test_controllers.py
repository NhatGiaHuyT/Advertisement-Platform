
from unittest.mock import AsyncMock

import pytest

from src.application.service.users import UserService, CreateUserInput, CreateUserDTO
from src.modules.users.controller import CreateUsersController


@pytest.mark.asyncio
async def test_create_user_DTO():
    fake_user_service = AsyncMock(spec=UserService)
    fake_user_service.create_user.return_value = CreateUserDTO(
        first_name="John",
        last_name="Doe",
        username="johndoe",
        email="johndoe@example.com",
    )

    request = CreateUserInput(
        first_name="John",
        last_name="Doe",
        username="johndoe",
        email="johndoe@example.com",
        password="johndoepassword"
    )

    controller = CreateUsersController(user_service=fake_user_service)

    result = await controller.handle(request)

    fake_user_service.create_user.assert_called_once_with(request)

    assert isinstance(result, CreateUserDTO)

    response_data = vars(result) 
    
    assert response_data.get("first_name") == "John"
    assert response_data.get("last_name") == "Doe"
    assert response_data.get("username") == "johndoe"
    assert response_data.get("email") == "johndoe@example.com"

    assert "password" not in response_data
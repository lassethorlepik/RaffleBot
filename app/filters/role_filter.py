from aiogram.filters import Filter
from aiogram import types
from typing import Union
from app.db.operations import get_user_by_role

class RoleCheck(Filter):
    def __init__(self, role: str) -> None:
        self.role = role

    async def __call__(self, query_or_message: Union[types.Message, types.CallbackQuery]) -> bool:  
        if self.role == "admin":  # role = 1 - admin
            return query_or_message.from_user.id in (await get_user_by_role("admin"))
        elif  self.role == "customer":  # role = 0 - customer
            return query_or_message.from_user.id in (await get_user_by_role("customer"))
        else:
            return False

async def role_check_function(query_or_message_id, role) -> bool:  
        if role == "admin":
            return query_or_message_id in (await get_user_by_role("admin"))
        elif  role == "customer":
            return query_or_message_id in (await get_user_by_role("customer"))
        else:
            return False
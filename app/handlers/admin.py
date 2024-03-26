from aiogram import types, Router
from app.loader import dp, bot
from app.db.operations import *
from app.keyboards.reply import *
from aiogram.filters.command import Command
from app.filters.role_filter import RoleCheck

router = Router()

# ADMIN COMMANDS

@router.message(Command("code"), RoleCheck("admin"))  # This always needs to be secure, as it generates new valid codes to enter the raffle
async def get_code(message: types.Message):
    try:
        code = generate_raffle_code()
        try:
            add_code_to_db(code)
        except Exception as e:
            print(f"ERROR ADDING CODE TO DB: {e}")
            await message.answer("An error occured while adding code to database!")
            return
        await message.answer(f"Code: `{code}`", parse_mode="MarkdownV2")
    except Exception as e:
        print(f"ERROR GENERATING CODE: {e}")
        await message.answer("An error occured while generating the code.")

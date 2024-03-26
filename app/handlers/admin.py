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
    "Generate a new code and send it to the admin."
    try:
        code = await generate_raffle_code()
        try:
            await add_code_to_db(code)
        except Exception as e:
            print(f"ERROR ADDING CODE TO DB: {e}")
            await message.answer("An error occured while adding code to database!")
            return
        await message.answer(f"Code: `{code}`", parse_mode="MarkdownV2")
    except Exception as e:
        print(f"ERROR GENERATING CODE: {e}")
        await message.answer("An error occured while generating the code.")


# Catch-all text message handler
@router.message(Command("start"))
async def catch_invalid_message(message: types.Message):
    "Respond to start command"
    await message.answer("Welcome, this is the raffle bot!\nEnter the raffle with /redeem <your-code>")


# Catch-all text message handler
@router.message()
async def catch_invalid_message(message: types.Message):
    "Catch any invalid messages from user."
    if await get_user_role(message.from_user.id) == 1:
        await message.answer("This is not a recognized command.\n/code to generate a valid code.\n/redeem <your-code> to enter the raffle.\n/whoami to check your user info.")
    else:
        await message.answer("This is not a recognized command.\nUse /redeem <your-code> to enter the raffle.")
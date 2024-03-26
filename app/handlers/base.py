import asyncio
from aiogram import Router, types
from app.loader import dp, bot
import app.db.operations
from app.db.operations import *
from app.keyboards.reply import *
from aiogram.filters.command import Command

router = Router()

# BASE COMMANDS (no permissions needed)


@router.message(Command("redeem"))
async def redeem(message: types.Message):
    "Redeem a code."
    user_id = message.from_user.id
    try:
        # Parsing stage with enhanced user input handling
        parts = message.text.strip().split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            await message.answer("You did not pass your code as an argument.\nUse /redeem <your-code> to enter the raffle.")
            return
        
        code = parts[1].strip()
        
        # Stop if code is longer than max length for generated codes.
        if len(code) > app.db.operations.CODE_LENGTH:
            await message.answer("The code you entered is invalid.")
            return
        
        # Redeeming stage with retry logic
        attempt = 0
        max_attempts = 3
        while attempt < max_attempts:
            try:
                attempt += 1
                success = await redeem_code(code, user_id)
                if success:
                    await message.answer("Your code has been successfully redeemed!")
                else:
                    await message.answer("The code you entered is invalid.")
                break
            except Exception as e:
                if attempt < max_attempts:
                    await asyncio.sleep(2 ** attempt)  # Exponential back-off
                else:
                    print(f"Final attempt failed for user {user_id} with code '{code}': {e}")
                    await message.answer("We're experiencing technical difficulties. Don't worry, we did not mark your code as used, please try again later.")
    except Exception as e:
        print(f"Unexpected error during code redemption for user {user_id}: {e}")
        await message.answer("We're experiencing technical difficulties! Don't worry, we did not mark your code as used, please try again later.")


@router.message(Command("whoami"))
async def who_am_i(message: types.Message):
    "Output info about the querying user."
    user_id = message.from_user.id
    username = await get_username(user_id)
    role = await get_user_role(user_id)
    await message.answer(f"Your name is {username}\nYour id is {user_id}\nYour role level is {role}")

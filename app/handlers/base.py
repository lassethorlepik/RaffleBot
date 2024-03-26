import asyncio
from aiogram import types, Router
from app.loader import dp, bot
from app.db.operations import *
from app.keyboards.reply import *
from aiogram.filters.command import Command

router = Router()

MAX_LENTH_OF_VALID_CODE = 8

# BASE COMMANDS (no permissions needed)


@router.message(Command("redeem"))
async def redeem(message: types.Message):
    user_id = message.from_user.id
    try:
        # Parsing stage with enhanced user input handling
        parts = message.text.strip().split(maxsplit=1)
        if len(parts) < 2 or not parts[1].strip():
            await message.answer("You did not pass your code as an argument. Use /redeem <your-code> to enter the raffle.")
            return
        
        code = parts[1].strip()
        
        # Stop if code is longer than max length for generated codes.
        if len(code) > MAX_LENTH_OF_VALID_CODE:
            await message.answer("The code you entered is invalid.")
            return

        await message.answer("Processing, please wait...")
        
        # Redeeming stage with retry logic
        attempt = 0
        max_attempts = 3
        while attempt < max_attempts:
            try:
                attempt += 1
                success = redeem_code(code, user_id)
                if success:
                    await message.answer("Your code has been successfully redeemed!")
                else:
                    await message.answer("This code has been used already!")
                break
            except Exception as e:
                if attempt < max_attempts:
                    await asyncio.sleep(2 ** attempt)  # Exponential back-off
                else:
                    print(f"Final attempt failed for user {user_id} with code '{code}': {e}")
                    await message.answer("We're experiencing technical difficulties. Don't worry, we did not mark the code as used, please try again later.")
    except Exception as e:
        print(f"Unexpected error during code redemption for user {user_id}: {e}")
        await message.answer("We're experiencing technical difficulties! Don't worry, we did not mark the code as used, please try again later.")


# Catch-all text message handler
@dp.message_handler(content_types=['text'])
async def catch_invalid_message(message: types.Message):
    # Respond to any text not caught by the above command handlers
    await message.answer("This is not a recognized command. Use /raffle <your-code> to enter the raffle.")

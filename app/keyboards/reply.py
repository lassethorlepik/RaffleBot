from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import DialogManager
from app.loader import bot

from app.db.operations import get_user_role

MAIN_MENU_BUTTON_TEXT = "Main menu"

def reply_row_menu(items):
    row = [types.KeyboardButton(text=item) for item in items]
    return types.ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def reply_column_menu(buttons):
    builder = ReplyKeyboardBuilder()
    for button in buttons:
        builder.add(types.KeyboardButton(text=button))
    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)


async def get_menu(message): # get UI buttons
    role = await get_user_role(message.from_user.id)
    if role is None:
        return get_main_menu_keyboard()
    all_keys = ["Button"]
    builder = ReplyKeyboardBuilder()  
    builder.add(types.KeyboardButton(text=all_keys[0]))

    # Return the built markup
    return builder.as_markup(resize_keyboard=True)


def get_main_menu_keyboard():
    keyboard = reply_column_menu([MAIN_MENU_BUTTON_TEXT])
    return keyboard


async def main_menu_handler(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.message.answer(MAIN_MENU_BUTTON_TEXT, reply_markup=await get_menu(callback.message))

import logging
from datetime import datetime
from pathlib import Path
from app.loader import bot, dp
from app.db import database
from app import loop
from app.handlers import base, admin
from aiogram_dialog import setup_dialogs

async def main():
    dp.include_routers(base.router, admin.router)
    setup_dialogs(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    log_name = f'logs/{datetime.now().strftime("%Y-%m-%d")}.log'
    Path(log_name).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_name,
        filemode="a"
    )
    loop.run_until_complete(database.create_pool()) # that was utterly freaking stupid
    loop.run_until_complete(main())
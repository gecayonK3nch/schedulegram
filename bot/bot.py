import asyncio
import logging
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler # type: ignore
from apscheduler.triggers.cron import CronTrigger # type: ignore
from cfg_parser import config
from handlers import keyboard_handler, messages_handler, inlineMode_handler, users_handler, on_startup_handler
from database.db_usage import clearing_db, create_users_table

# Инициализация бота с токеном из конфигурации
bot = Bot(token=config.bot_token.get_secret_value()) 


async def main():
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    # Запуск планировщика задач (очистка базы данных по расписанию)
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.start()
    scheduler.add_job( # type: ignore
        clearing_db,
        CronTrigger(hour=0, minute=0),
        id="clear_db",
        replace_existing=True,
    )
    # Создание таблицы пользователей, если не существует
    await create_users_table()

    # Инициализация диспетчера и подключение роутеров
    dp = Dispatcher()

    dp.include_routers(keyboard_handler.router,
                       messages_handler.router,
                       inlineMode_handler.router,
                       users_handler.router,
                       on_startup_handler.router)

    # Удаление вебхука и запуск polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot) # type: ignore


if __name__ == "__main__":
    # Запуск основного цикла бота
    asyncio.run(main())

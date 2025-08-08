import asyncio
import logging
from aiogram import Router
from database.db_usage import get_users
import bot

# Роутер для обработки событий запуска бота
router = Router()

# Отправка сообщения всем пользователям о перезапуске бота
@router.startup()
async def send_restart_message():
    users = await get_users()
    for user_id in users:
        try:
            await bot.bot.send_message(user_id, "Бот перезапущен. Для корректной работы выполните команду /start.") #type: ignore
        except Exception as e:
            logging.error(f"Failed to send restart message to user {user_id}: {e}")
        await asyncio.sleep(0.1)

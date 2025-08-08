from aiogram import Router, F
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
import time
from states.states import ChoosingDirection
from database.db_usage import get_schedule, add_user
from database.get_stations import stations
import bot
from keyboards.keyboards import get_main_kb
from messages import START_MSG

# Роутер для обработки входящих сообщений
router = Router()

# Обработка команды /start
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await add_user(user_id=message.from_user.id) #type: ignore
    await state.update_data(chosen_from=None,
                            chosen_to=None,
                            chosen_date=None,
                            show_gone=False)
    id = await message.answer(START_MSG, reply_markup=await get_main_kb(state=state))
    await state.update_data(main_msg=id.message_id)

# Обработка выбора станции отправления или прибытия
@router.message(F.state.in_([ChoosingDirection.choosing_from, ChoosingDirection.choosing_to]) and F.text.in_(stations.keys()))
async def chosen_dir(message: Message, state: FSMContext):
    if await state.get_state() == ChoosingDirection.choosing_from:
        await state.update_data(chosen_from=message.text)
    else:
        await state.update_data(chosen_to=message.text)
    data = await state.get_data()
    date = data['chosen_date']
    with suppress(TelegramBadRequest):
        if all((data['chosen_from'], data['chosen_to'], data['chosen_date'])):
            text = get_schedule(data['chosen_from'], data['chosen_to'], date.strftime("%Y-%m-%d"), data['show_gone']) # type: ignore
            await bot.bot.edit_message_text(text=text, chat_id=message.from_user.id, message_id=data['main_msg'], reply_markup=await get_main_kb(state=state)) # type: ignore
        else:
            await bot.bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=data['main_msg'], reply_markup=await get_main_kb(state=state)) # type: ignore
    await message.delete()

# Обработка всех остальных сообщений
@router.message()
async def any_msg(message: Message):
    reply = await message.reply(text="Я не знаю, как на это отвечать :(")
    time.sleep(5)
    await reply.delete()
    await message.delete()

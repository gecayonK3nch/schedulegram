from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale #type: ignore
from datetime import datetime
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from states.states import ChoosingDirection
import bot
from database.db_usage import get_schedule
from keyboards.keyboards import get_main_kb

# Роутер для обработки callback-запросов с клавиатуры
router = Router()

# Обработка выбора станции отправления
@router.callback_query(F.data == "choosing_from")
async def keyboard_from(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChoosingDirection.choosing_from)
    await callback.answer(
        text="Пожалуйста, введите место отправления при помощи кнопки снизу",
        show_alert=True
    )

# Обработка выбора станции прибытия
@router.callback_query(F.data == "choosing_to")
async def keyboard_to(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ChoosingDirection.choosing_to)
    await callback.answer(
        text="Пожалуйста, введите место прибытия при помощи кнопки снизу",
        show_alert=True
    )

# Обработка выбора даты отправления (открытие календаря)
@router.callback_query(F.data == "choosing_date")
async def keyboard_date(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer( # type: ignore
        text="Пожалуйста, выберите дату отправления",
        reply_markup=await SimpleCalendar(locale=await get_user_locale(callback.from_user)).start_calendar()
    )
    await state.set_state(ChoosingDirection.choosing_date)
    await callback.answer()

# Обработка выбора даты в календаре
@router.callback_query(SimpleCalendarCallback.filter())
async def calendar_chosen(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(locale=await get_user_locale(callback.from_user), show_alerts=True)
    calendar.set_dates_range(datetime(2025, 1, 1), datetime(2028, 12, 31))
    selected, date = await calendar.process_selection(callback, callback_data) #type: ignore
    if selected:
        await state.update_data(chosen_date=date)
        await state.set_state(None)
        data = await state.get_data()
        await callback.message.delete() # type: ignore
        with suppress(TelegramBadRequest):
            if all((data['chosen_from'], data['chosen_to'], data['chosen_date'])):
                text = get_schedule(data['chosen_from'], data['chosen_to'], date.strftime("%Y-%m-%d"), data['show_gone']) # type: ignore
                await bot.bot.edit_message_text(text=text, chat_id=callback.from_user.id, message_id=data['main_msg'], reply_markup=await get_main_kb(state=state)) # type: ignore
            else:
                await bot.bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=data['main_msg'], reply_markup=await get_main_kb(state=state)) # type: ignore
        await callback.answer(
            text=f"Вы выбрали {date.strftime('%d.%m.%Y')}", # type: ignore
            show_alert=True
        )

# Обработка переключения отображения ушедших поездов
@router.callback_query(F.data == "show_gone")
async def show_gone(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    date = data['chosen_date']
    await state.update_data(show_gone=not data['show_gone'])
    data = await state.get_data()
    with suppress(TelegramBadRequest):
            if all((data['chosen_from'], data['chosen_to'], data['chosen_date'])):
                text = get_schedule(data['chosen_from'], data['chosen_to'], date.strftime("%Y-%m-%d"), data['show_gone']) # type: ignore
                await bot.bot.edit_message_text(text=text, chat_id=callback.from_user.id, message_id=data['main_msg'], reply_markup=await get_main_kb(state=state)) # type: ignore
            else:
                await bot.bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=data['main_msg'], reply_markup=await get_main_kb(state=state)) # type: ignore
    await callback.answer()

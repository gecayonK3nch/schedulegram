from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from database.get_stations import stations


# Получение корректного текста для кнопки в зависимости от значения
def get_right_text(object: str) -> str:
    if not object:
        return "Не выбрано"
    elif type(object) != str:
        return object.strftime("%d.%m.%Y") #type: ignore
    return stations[object]


# Асинхронная функция генерации основной клавиатуры на основе состояния пользователя
async def get_main_kb(state: FSMContext):
    builder = InlineKeyboardBuilder()
    data = await state.get_data()
    builder.button(
        text=f"Отправление: {get_right_text(data['chosen_from'])}",
        callback_data="choosing_from"
    )
    builder.button(
        text=f"Прибытие: {get_right_text(data['chosen_to'])}",
        callback_data="choosing_to"
    )
    builder.button(
        text=f"Дата: {get_right_text(data['chosen_date'])}",
        callback_data="choosing_date"
    )
    builder.button(
        text="Показать ушедшие",
        callback_data="show_gone"
    )
    builder.button(
        text="🔃",
        callback_data="return"
    )
    builder.button(
        text="Ввести место",
        switch_inline_query_current_chat=""
    )

    builder.adjust(1)  # Располагаем кнопки в один столбец
    return builder.as_markup()

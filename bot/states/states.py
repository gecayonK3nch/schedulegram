from aiogram.fsm.state import StatesGroup, State

# Группа состояний для выбора направления и даты
class ChoosingDirection(StatesGroup):
    choosing_from = State()   # Состояние выбора станции отправления
    choosing_to = State()     # Состояние выбора станции прибытия
    choosing_date = State()   # Состояние выбора даты

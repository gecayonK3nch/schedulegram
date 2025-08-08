from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from database.get_stations import stations

# Роутер для обработки inline-запросов
router = Router()

# Обработка inline-запроса пользователя (поиск станции)
@router.inline_query()
async def inline_query_handler(inline_query: InlineQuery):
    results: list[InlineQueryResultArticle] = []
    # Сортируем станции по длине и алфавиту, фильтруем по запросу пользователя
    for station_code, station_name in sorted(sorted(stations.items(), key=lambda x: x[1]), key=lambda y: len(y[1])):
        if (station_name.lower().startswith(inline_query.query.lower()) or (inline_query.query.lower() in station_name.lower())) and len(results) < 50:
            results.append(
                InlineQueryResultArticle(
                    id=station_code,
                    title=station_name,
                    input_message_content=InputTextMessageContent(
                        message_text=station_code,
                        parse_mode='HTML'
                    )
                )
            )
        elif len(results) >= 50:
            break
    # Отправляем пользователю не более 50 результатов
    await inline_query.answer(results, cache_time=86400, is_personal=False) #type: ignore

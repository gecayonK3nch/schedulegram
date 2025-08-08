from aiogram import F, Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import ChatMemberUpdated
from database.db_usage import user_banned, add_user

# Роутер для обработки событий изменения статуса пользователя в чате
router = Router()
router.my_chat_member.filter(F.chat.type == "private")

# Обработка блокировки бота пользователем
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def bot_blocked(event: ChatMemberUpdated):
    await user_banned(event.from_user.id)
    print(f"User @{event.from_user.username} blocked bot (id: {event.from_user.id})")

# Обработка разблокировки бота пользователем
@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def bot_unblocked(event: ChatMemberUpdated):
    await add_user(event.from_user.id)
    print(f"User @{event.from_user.username} unblocked bot (id: {event.from_user.id})")

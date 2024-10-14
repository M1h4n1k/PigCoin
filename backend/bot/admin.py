from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database import models
from .loader import bot

from database.loader import SessionLocal
from .loader import ADMINS


async def setup_spam_message(message: Message, state: FSMContext):
    if message.from_user.id not in ADMINS:
        return
    entities = message.entities[1:]
    for ent in entities:
        ent.offset -= 6

    await state.set_data({
        'spam_text': message.text.replace('/spam ', ''),
        'spam_entities': entities
    })
    await message.answer(
        text=message.text.replace('/spam ', ''),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='Yes ✅', callback_data='accept_spam'),
        ]]),
        entities=entities
    )


async def send_spam_message(call: CallbackQuery, state: FSMContext):
    await call.answer()
    if call.from_user.id not in ADMINS:
        return
    spam_data = await state.get_data()
    text = spam_data.get('spam_text')
    entities = spam_data.get('spam_entities')
    await state.clear()
    db = SessionLocal()
    user_ids = db.query(models.User.tg_id).all()
    db.close()
    success_count = 0
    await call.message.answer(f'Starting spam to all users, {len(user_ids)} users in total')
    for user in user_ids:
        try:
            await bot.send_message(chat_id=user[0], text=text, entities=entities)
            success_count += 1
        except Exception:
            pass
    await call.message.answer(f'Done, the message was received by {success_count} users')

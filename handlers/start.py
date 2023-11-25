from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
import data.keyboards.inline as ikb
from utils.bot_functions.back import *
from data.media.texts import start_text


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer(text=start_text, reply_markup=await ikb.start())

@dp.callback_query_handler(state='*', text_startswith='back_')
async def back(call: types.CallbackQuery, state: FSMContext):
	await call.answer('')

	bot_page = call.data.split('back_')[1]
	bot_pages = {
		'start': back_to_start,
		'list_books': back_to_list_books,
		'books_categories': back_to_books_categories,
		'books_by_categories': back_to_books_by_categories,
		'all_books': back_to_all_books
	}

	await bot_pages[bot_page](call, state)
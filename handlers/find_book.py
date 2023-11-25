from aiogram import types
from aiogram.dispatcher import FSMContext

from data.media.texts import start_text
from loader import dp, db
import data.keyboards.inline as ikb
from data.states import FindBook
from utils.bot_functions.bot_functions import delete_book


@dp.callback_query_handler(text='find_book')
async def find_book(call: types.CallbackQuery):
	await call.answer('')
	await FindBook.results.set()
	await call.message.answer(text='Введите ключевое слово или фразу для поиска в полях "Название" и "Автор":',
	                          reply_markup=await ikb.back(bot_page='start'))


@dp.message_handler(state=FindBook.results)
async def find_book_results(message: types.Message, state: FSMContext):
	text = message.text.lower()
	books = await db.find_book_results(text=text)
	if books:
		await FindBook.books_by_results.set()
		await state.update_data(books=books, text=text)
		await message.answer(text=f"⚜️ Результаты поиска по запросу - {text}:", reply_markup=await ikb.books(bot_page='start',
                                                                                books=books,
                                                                                current_page=1))
	else:
		await state.finish()
		await message.answer(text='⛔️ По вашему запросу ничего не найдено.')
		await message.answer(text=start_text, reply_markup=await ikb.start())


@dp.callback_query_handler(state=FindBook.books_by_results)
async def books_by_results(call: types.CallbackQuery, state: FSMContext):
	await call.answer('')

	if call.data.startswith('goto_'):
		current_page = int(call.data.split('goto_')[1])
		books = (await state.get_data())['books']
		try:
			await call.message.edit_reply_markup(reply_markup=await ikb.books(bot_page='start',
			                                                                  books=books,
			                                                                  current_page=current_page))
		except:
			pass

	elif call.data.startswith('book_'):
		book_id = int(call.data.split('book_')[1])
		book = await db.get_book(book_id=book_id)
		text = f"📕 Книга: {book['title']}\n\n" \
		       f"👨‍💼 Автор: {book['author']}\n\n" \
		       f"💈 Жанр: {book['category']}\n\n" \
		       f"📜 Описание: {book['description']}"
		await call.message.edit_text(text=text,
		                             reply_markup=await ikb.book(bot_page='books_by_results', book_id=book_id))


@dp.callback_query_handler(state=FindBook.in_book)
async def in_book(call: types.CallbackQuery, state: FSMContext):
	if call.data.startswith('delete_book_'):
		await delete_book(call, state, db, start_text, ikb)

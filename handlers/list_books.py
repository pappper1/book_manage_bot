from aiogram import types
from aiogram.dispatcher import FSMContext

from data.media.texts import start_text
from loader import dp, db
import data.keyboards.inline as ikb
from data.states import BookList


@dp.callback_query_handler(text='list_books')
async def list_books(call: types.CallbackQuery, state: FSMContext):
	await BookList.choose_type.set()
	await call.message.edit_text(text='🔻 Выберите способ отображения книг:',
	                             reply_markup=await ikb.select_display_books_type(bot_page='start'))


@dp.callback_query_handler(state=BookList.choose_type)
async def select_display_books_type(call: types.CallbackQuery, state: FSMContext):
	await call.answer('')

	if call.data == 'all_books':
		await BookList.all_books.set()
		books = await db.get_all_books()
		await call.message.edit_text(text='🗂 Все книги:', reply_markup=await ikb.books(bot_page='list_books',
		                                                                             books=books,
		                                                                             current_page=1))

	elif call.data == 'books_by_categories':
		await BookList.books_categories.set()
		categories = await db.get_categories()
		await call.message.edit_text(text='🔻 Выберите жанр, книги которого вы хотите увидеть:',
		                             reply_markup=await ikb.book_categories(bot_page='list_books',
		                                                                      categories=categories,
		                                                                      current_page=1))


@dp.callback_query_handler(state=BookList.books_categories)
async def book_categories(call: types.CallbackQuery, state: FSMContext):
	await call.answer('')

	if call.data.startswith('goto_'):
		page = int(call.data.split('goto_')[1])
		categories = await db.get_categories()
		await call.message.edit_reply_markup(reply_markup=await ikb.book_categories(bot_page='list_books',
		                                                                            categories=categories,
		                                                                            current_page=page))

	elif call.data.startswith('category_'):
		await BookList.books_by_categories.set()
		category = call.data.split('category_')[1]
		books = await db.get_books_by_category(category=category)
		await state.update_data(category=category)
		await call.message.edit_text(text=f'📚 Книги по жанру "{category}":',
		                             reply_markup=await ikb.books(bot_page='books_categories',
		                                                          books=books,
		                                                          current_page=1))


@dp.callback_query_handler(state=BookList.books_by_categories)
async def books_by_categories(call: types.CallbackQuery, state: FSMContext):
	await call.answer('')

	if call.data.startswith('goto_'):
		page = int(call.data.split('goto_')[1])
		category = (await state.get_data())['category']
		books = await db.get_books_by_category(category=category)
		await call.message.edit_reply_markup(reply_markup=await ikb.books(bot_page='books_categories',
		                                                                  books=books,
		                                                                  current_page=page))

	elif call.data.startswith('book_'):
		await BookList.in_book.set()
		book_id = int(call.data.split('book_')[1])
		book = await db.get_book(book_id=book_id)
		text = f"Книга: {book['title']}\n\n" \
		       f"Автор: {book['author']}\n\n" \
		       f"Жанр: {book['category']}\n\n" \
		       f"Описание: {book['description']}"
		await call.message.edit_text(text=text,
		                             reply_markup=await ikb.book(bot_page='books_by_categories' ,book_id=book_id))


@dp.callback_query_handler(state=BookList.in_book)
async def in_book(call: types.CallbackQuery, state: FSMContext):
	await call.answer('')

	if call.data.startswith('delete_book_'):
		book_id = int(call.data.split('delete_book_')[1])
		await state.finish()
		await db.delete_book(book_id=book_id)
		await call.answer(text='🔰 Книга удалена!', show_alert=True)
		await call.message.answer(text=start_text, reply_markup=await ikb.start())
		await call.message.delete()


@dp.callback_query_handler(state=BookList.all_books)
async def all_books(call: types.CallbackQuery, state: FSMContext):
	await call.answer('')

	if call.data.startswith('goto_'):
		page = int(call.data.split('goto_')[1])
		books = await db.get_all_books()
		await call.message.edit_reply_markup(reply_markup=await ikb.books(bot_page='list_books',
		                                                                  books=books,
		                                                                  current_page=page))

	elif call.data.startswith('book_'):
		await BookList.in_book.set()
		book_id = int(call.data.split('book_')[1])
		book = await db.get_book(book_id=book_id)
		text = f"📕 Книга: {book['title']}\n\n" \
		       f"👨‍💼 Автор: {book['author']}\n\n" \
		       f"💈 Жанр: {book['category']}\n\n" \
		       f"📜 Описание: {book['description']}"
		await call.message.edit_text(text=text,
		                             reply_markup=await ikb.book(bot_page='all_books' ,book_id=book_id))
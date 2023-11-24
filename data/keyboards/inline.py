from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def start():
	ikb = InlineKeyboardMarkup(row_width=2)

	find_book_button = InlineKeyboardButton(text='🔎 Поиск', callback_data='find_book')
	list_books_button = InlineKeyboardButton(text='📚 Книги', callback_data='list_books')
	create_book_button = InlineKeyboardButton(text='➕ Добавить книгу', callback_data='create_book')

	ikb.add(list_books_button).add(find_book_button, create_book_button)
	return ikb
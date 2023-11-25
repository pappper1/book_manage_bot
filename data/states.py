from aiogram.dispatcher.filters.state import State, StatesGroup

class NewBook(StatesGroup):
	title = State()
	author = State()
	description = State()
	category = State()

class BookList(StatesGroup):
	choose_type = State()

	all_books = State()
	books_categories = State()

	books_by_categories = State()

	in_book = State()
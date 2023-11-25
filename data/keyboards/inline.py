from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start():
	ikb = InlineKeyboardMarkup(row_width=2)

	find_book_button = InlineKeyboardButton(text='🔎 Поиск', callback_data='find_book')
	list_books_button = InlineKeyboardButton(text='📚 Книги', callback_data='list_books')
	create_book_button = InlineKeyboardButton(text='➕ Добавить книгу', callback_data='create_book')

	ikb.add(list_books_button).add(find_book_button, create_book_button)
	return ikb


async def book_categories(bot_page: str, categories, current_page: int):
	ikb = InlineKeyboardMarkup()
	categories_on_page = 6
	pages = (len(categories) // categories_on_page) if len(categories) >= categories_on_page \
		else (len(categories) // categories_on_page)+1
	next_page = (current_page + 1) if current_page != pages else 1
	previous_page = (current_page - 1) if current_page != 1 else pages

	previous_page_button = InlineKeyboardButton(text='🔚', callback_data=f"goto_{previous_page}")
	current_page_button = InlineKeyboardButton(text=f"{current_page}", callback_data='selected')
	next_page_button = InlineKeyboardButton(text='🔜', callback_data=f"goto_{next_page}")
	back_button = InlineKeyboardButton(text='🔚 Назад', callback_data=f"back_{bot_page}")

	page = current_page - 1
	categories_for_page = categories[page*categories_on_page:categories_on_page*current_page]
	for category in categories_for_page:
		ikb.add(InlineKeyboardButton(text=f"{category['category_title']}",
		                             callback_data=f"category_{category['category_title']}"))

	ikb.add(previous_page_button, current_page_button, next_page_button).add(back_button)
	return ikb


async def select_display_books_type(bot_page: str):
	ikb = InlineKeyboardMarkup(row_width=1)

	all_books_button = InlineKeyboardButton(text='🗂 Все', callback_data='all_books')
	categories_books_button = InlineKeyboardButton(text='💈 По жанрам', callback_data='books_by_categories')
	back_button = InlineKeyboardButton(text='🔚 Назад', callback_data=f"back_{bot_page}")

	ikb.add(all_books_button, categories_books_button, back_button)
	return ikb


async def books(bot_page: str, books, current_page: int):
	ikb = InlineKeyboardMarkup()
	books_on_page = 6
	pages = (len(books) // books_on_page) if len(books) >= books_on_page else (len(books) // books_on_page)+1
	next_page = (current_page + 1) if current_page != pages else 1
	previous_page = (current_page - 1) if current_page != 1 else pages

	previous_page_button = InlineKeyboardButton(text='🔚', callback_data=f"goto_{previous_page}")
	current_page_button = InlineKeyboardButton(text=f"{current_page}", callback_data='selected')
	next_page_button = InlineKeyboardButton(text='🔜', callback_data=f"goto_{next_page}")
	back_button = InlineKeyboardButton(text='🔚 Назад', callback_data=f"back_{bot_page}")

	page = current_page - 1
	books_for_page = books[page*books_on_page:books_on_page*current_page]
	for book in books_for_page:
		ikb.add(InlineKeyboardButton(text=f"{book['title']}",
		                             callback_data=f"book_{book['id']}"))

	ikb.add(previous_page_button, current_page_button, next_page_button).add(back_button)
	return ikb


async def book(bot_page: str ,book_id: int):
	ikb = InlineKeyboardMarkup(row_width=1)

	delete_book_button = InlineKeyboardButton(text='🗑 Удалить', callback_data=f"delete_book_{book_id}")
	back_button = InlineKeyboardButton(text='🔚 Назад', callback_data=f"back_{bot_page}")

	ikb.add(delete_book_button, back_button)
	return ikb

async def back(bot_page: str):
	ikb = InlineKeyboardMarkup(row_width=1)

	back_button = InlineKeyboardButton(text='🔚 Назад', callback_data=f"back_{bot_page}")

	ikb.add(back_button)
	return ikb
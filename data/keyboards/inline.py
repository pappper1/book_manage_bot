from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def start():
	ikb = InlineKeyboardMarkup(row_width=2)

	find_book_button = InlineKeyboardButton(text='🔎 Поиск', callback_data='find_book')
	list_books_button = InlineKeyboardButton(text='📚 Книги', callback_data='list_books')
	create_book_button = InlineKeyboardButton(text='➕ Добавить книгу', callback_data='create_book')

	ikb.add(list_books_button).add(find_book_button, create_book_button)
	return ikb

async def back(bot_page: str):
	ikb = InlineKeyboardMarkup(row_width=1)

	back_button = InlineKeyboardButton(text='🔚 Назад', callback_data=f"back_{bot_page}")

	ikb.add(back_button)
	return ikb

async def book_categories(bot_page: str, categories, current_page: int):
	ikb = InlineKeyboardMarkup(row_width=3)
	categories_on_page = 6
	pages = (len(categories) // categories_on_page) if len(categories) <= categories_on_page \
		else (len(categories) // categories_on_page)+1
	next_page = (current_page + 1) if current_page != pages else 1
	previous_page = (current_page - 1) if current_page != 1 else pages

	previous_page_button = InlineKeyboardButton(text='Предыдущая', callback_data=f"goto_{previous_page}")
	current_page_button = InlineKeyboardButton(text=f"{current_page}", callback_data='selected')
	next_page_button = InlineKeyboardButton(text='Следующая', callback_data=f"goto_{next_page}")
	back_button = InlineKeyboardButton(text='🔚 Назад', callback_data=f"back_{bot_page}")

	page = current_page - 1
	categories_for_page = categories[page*categories_on_page:categories_on_page*current_page]
	for category in categories_for_page:
		ikb.add(InlineKeyboardButton(text=f"{category['category_title']}",
		                             callback_data=f"category_{category['category_title']}"))

	ikb.add(previous_page_button, current_page_button, next_page_button).add(back_button)
	return ikb
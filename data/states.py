from aiogram.dispatcher.filters.state import State, StatesGroup

class NewBook(StatesGroup):
	title = State()
	author = State()
	description = State()
	category = State()
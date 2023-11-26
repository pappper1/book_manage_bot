from aiogram.dispatcher.filters.state import State, StatesGroup


# Состояния создания книги
class NewBook(StatesGroup):
    title = State()
    author = State()
    description = State()
    category = State()


# Состояния просмотра книг
class BookList(StatesGroup):
    choose_type = State()

    all_books = State()
    books_categories = State()
    add_category = State()

    books_by_categories = State()

    in_book = State()


# Состояния поиска книг
class FindBook(StatesGroup):
    results = State()

    books_by_results = State()

    in_book = State()

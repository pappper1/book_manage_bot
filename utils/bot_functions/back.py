import data.keyboards.inline as ikb
from data.media.texts import *
from data.states import BookList, FindBook
from loader import db


# Назад к стартовому меню
async def back_to_start(call, state):
    await state.finish()

    await call.message.edit_text(text=start_text, reply_markup=await ikb.start())


# Назад к выбору способа отображения книг
async def back_to_list_books(call, state):
    await BookList.choose_type.set()
    await call.message.edit_text(
        text=display_books_type_text,
        reply_markup=await ikb.select_display_books_type(bot_page="start"),
    )


# Назад к выбору жанра книг
async def back_to_books_categories(call, state):
    await BookList.books_categories.set()
    categories = await db.get_categories()
    await call.message.edit_text(
        text=category_choose_text,
        reply_markup=await ikb.book_categories(bot_page="list_books", categories=categories, current_page=1,
                                               mode='book_list'),
    )


# Назад к выбору книги по жанру
async def back_to_books_by_categories(call, state):
    await BookList.books_by_categories.set()
    category = (await state.get_data())["category"]
    books = await db.get_books_by_category(category=category)
    await call.message.edit_text(
        text=f'📚 Ниже отображены книги по жанру "{category}":',
        reply_markup=await ikb.books(
            bot_page="books_categories", books=books, current_page=1
        ),
    )


# Назад ко всем книгам
async def back_to_all_books(call, state):
    await BookList.all_books.set()
    books = await db.get_all_books()
    await call.message.edit_text(
        text="🗂 Ниже отображены все добавленные книги:",
        reply_markup=await ikb.books(
            bot_page="list_books", books=books, current_page=1
        ),
    )


# Назад к результатам поиска
async def back_to_books_by_results(call, state):
    await FindBook.books_by_results.set()
    data = await state.get_data()
    text = data["text"]
    books = data["books"]
    await call.message.edit_text(
        text=f"⚜️ Результаты поиска по запросу - {text}:",
        reply_markup=await ikb.books(bot_page="start", books=books, current_page=1),
    )

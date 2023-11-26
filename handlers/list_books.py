from aiogram import types
from aiogram.dispatcher import FSMContext

from data.media.texts import *
from loader import dp, db
import data.keyboards.inline as ikb
from data.states import BookList
from utils.bot_functions.bot_functions import delete_book


# Выбор способа отображения книг
@dp.callback_query_handler(text="list_books")
async def list_books(call: types.CallbackQuery):
    await BookList.choose_type.set()
    await call.message.edit_text(
        text=display_books_type_text,
        reply_markup=await ikb.select_display_books_type(bot_page="start"),
    )


# Отображение книг если выбран пункт Все и отображение жанров если выбрано по жанрам
@dp.callback_query_handler(state=BookList.choose_type)
async def select_display_books_type(call: types.CallbackQuery):
    if call.data == "all_books":
        books = await db.get_all_books()
        if len(books) != 0:
            await call.answer("")
            await BookList.all_books.set()
            await call.message.edit_text(
                text=all_books_text,
                reply_markup=await ikb.books(
                    bot_page="list_books", books=books, current_page=1
                ),
            )
        else:
            await call.answer(
                text=no_books_text, show_alert=True
            )

    elif call.data == "books_by_categories":
        await call.answer("")
        await BookList.books_categories.set()
        categories = await db.get_categories()
        await call.message.edit_text(
            text=category_choose_text,
            reply_markup=await ikb.book_categories(bot_page="list_books", categories=categories, current_page=1,
                                                   mode='book_list'),
        )


# Пагинация жанров, отображение книг в жанре и добавление нового жанра
@dp.callback_query_handler(state=BookList.books_categories)
async def book_categories(call: types.CallbackQuery, state: FSMContext):
    if call.data.startswith("goto_"):
        await call.answer("")
        page = int(call.data.split("goto_")[1])
        categories = await db.get_categories()
        try:
            await call.message.edit_reply_markup(
                reply_markup=await ikb.book_categories(bot_page="list_books", categories=categories, current_page=page,
                                                       mode='book_list')
            )
        except:
            pass

    elif call.data.startswith("category_"):
        category = call.data.split("category_")[1]
        books = await db.get_books_by_category(category=category)
        if len(books) != 0:
            await call.answer("")
            await BookList.books_by_categories.set()
            await state.update_data(category=category)
            await call.message.edit_text(
                text=f'{books_for_category_text} "{category}":',
                reply_markup=await ikb.books(
                    bot_page="books_categories", books=books, current_page=1
                ),
            )
        else:
            await call.answer(text=no_books_text, show_alert=True)

    elif call.data == "add_category":
        await BookList.add_category.set()
        await call.answer("")
        await call.message.edit_text(
            text=new_category_text,
            reply_markup=await ikb.back(bot_page="list_books"),
        )


# Добавление нового жанра
@dp.message_handler(state=BookList.add_category)
async def add_category(message: types.Message):
    category = message.text
    if len(category) > 256:
        await message.answer(
            text=max_lenght_text, reply_markup=await ikb.back(bot_page="list_books")
        )

    else:
        await BookList.books_categories.set()
        await db.add_category(title=category)
        await message.answer(text=f'✅ Жанр "{category}" успешно добавлен!')
        categories = await db.get_categories()
        await message.answer(
            text=category_choose_text,
            reply_markup=await ikb.book_categories(bot_page="list_books", categories=categories, current_page=1,
                                                   mode='book_list'),
        )


# Пагинация книг в выбранном жанре
@dp.callback_query_handler(state=BookList.books_by_categories)
async def books_by_categories(call: types.CallbackQuery, state: FSMContext):
    await call.answer("")

    if call.data.startswith("goto_"):
        page = int(call.data.split("goto_")[1])
        category = (await state.get_data())["category"]
        books = await db.get_books_by_category(category=category)
        try:
            await call.message.edit_reply_markup(
                reply_markup=await ikb.books(
                    bot_page="books_categories", books=books, current_page=page
                )
            )
        except:
            pass

    elif call.data.startswith("book_"):
        await BookList.in_book.set()
        book_id = int(call.data.split("book_")[1])
        book = await db.get_book(book_id=book_id)
        text = (
            f"📕 Книга: {book['title']}\n\n"
            f"👨‍💼 Автор: {book['author']}\n\n"
            f"💈 Жанр: {book['category']}\n\n"
            f"📜 Описание: {book['description']}"
        )
        await call.message.edit_text(
            text=text,
            reply_markup=await ikb.book(
                bot_page="books_by_categories", book_id=book_id
            ),
        )


# Удаление книги
@dp.callback_query_handler(state=BookList.in_book)
async def in_book(call: types.CallbackQuery, state: FSMContext):
    if call.data.startswith("delete_book_"):
        await delete_book(call, state, db, start_text, ikb)


# Отображение списка всех книг и отображение информации книги
@dp.callback_query_handler(state=BookList.all_books)
async def all_books(call: types.CallbackQuery):
    await call.answer("")

    if call.data.startswith("goto_"):
        page = int(call.data.split("goto_")[1])
        books = await db.get_all_books()
        try:
            await call.message.edit_reply_markup(
                reply_markup=await ikb.books(
                    bot_page="list_books", books=books, current_page=page
                )
            )
        except:
            pass

    elif call.data.startswith("book_"):
        await BookList.in_book.set()
        book_id = int(call.data.split("book_")[1])
        book = await db.get_book(book_id=book_id)
        text = (
            f"📕 Книга: {book['title']}\n\n"
            f"👨‍💼 Автор: {book['author']}\n\n"
            f"💈 Жанр: {book['category']}\n\n"
            f"📜 Описание: {book['description']}"
        )
        await call.message.edit_text(
            text=text,
            reply_markup=await ikb.book(bot_page="all_books", book_id=book_id),
        )

from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, db
import data.keyboards.inline as ikb
from data.states import NewBook
from data.media.texts import *


# Создание новой книги
@dp.callback_query_handler(text="create_book")
async def create_book(call: types.CallbackQuery, state: FSMContext):
    await NewBook.title.set()

    await call.message.edit_text(
        text=new_book_title_text, reply_markup=await ikb.back(bot_page="start")
    )


# Добавление названия для новой книги
@dp.message_handler(state=NewBook.title)
async def new_book_title(message: types.Message, state: FSMContext):
    title = message.text
    if len(title) > 256:
        await message.answer(
            text=max_lenght_text, reply_markup=await ikb.back(bot_page="start")
        )

    else:
        await NewBook.author.set()
        await state.update_data(title=title)

        await message.answer(
            text=new_book_author_text, reply_markup=await ikb.back(bot_page="start")
        )


# Добавление автора для новой книги
@dp.message_handler(state=NewBook.author)
async def new_book_author(message: types.Message, state: FSMContext):
    author = message.text
    if len(author) > 256:
        await message.answer(
            text=max_lenght_text, reply_markup=await ikb.back(bot_page="start")
        )

    else:
        await NewBook.description.set()
        await state.update_data(author=author)

        await message.answer(
            text=new_book_description_text,
            reply_markup=await ikb.back(bot_page="start"),
        )


# Добавление описания для новой книги
@dp.message_handler(state=NewBook.description)
async def new_book_description(message: types.Message, state: FSMContext):
    description = message.text
    categories = await db.get_categories()

    await NewBook.category.set()
    await state.update_data(description=description, categories=categories)
    await message.answer(
        text=new_book_category_text,
        reply_markup=await ikb.book_categories(
            bot_page="start", categories=categories, current_page=1
        ),
    )


# Добавление жанра для новой книги(с помощью своего жанра)
@dp.message_handler(state=NewBook.category)
async def new_book_category_mes(message: types.Message, state: FSMContext):
    category_title = message.text

    if len(category_title) > 256:
        await message.answer(
            text=max_lenght_text, reply_markup=await ikb.back(bot_page="start")
        )

    else:
        data = await state.get_data()
        title, author, description = data["title"], data["author"], data["description"]

        await state.finish()
        await db.add_category(title=category_title)
        await db.add_book(
            title=title, author=author, description=description, category=category_title
        )
        await message.answer(
            text=await new_book_added_text(title=title, category_title=category_title)
        )
        await message.answer(text=start_text, reply_markup=await ikb.start())


# Добавление жанра для новой книги(с помощью кнопок)
@dp.callback_query_handler(state=NewBook.category)
async def new_book_category_call(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if call.data.startswith("goto_"):
        categories = data["categories"]
        page = int(call.data.split("goto_")[1])

        await call.message.edit_reply_markup(
            reply_markup=await ikb.book_categories(
                bot_page="start",
                categories=categories,
                current_page=page,
                mode="add_book",
            )
        )

    elif call.data.startswith("category_"):
        category = call.data.split("category_")[1]
        title, author, description = data["title"], data["author"], data["description"]

        await state.finish()
        await db.add_book(
            title=title, author=author, description=description, category=category
        )
        await call.message.answer(
            text=await new_book_added_text(title=title, category_title=category)
        )
        await call.message.answer(text=start_text, reply_markup=await ikb.start())
        await call.message.delete()

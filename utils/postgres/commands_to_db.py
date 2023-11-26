from loguru import logger

from .postgress_handler import (
    postgres_do_query,
    postgres_select_all,
    postgres_select_one,
)


class Database:
    @staticmethod
    async def create_tables():
        await postgres_do_query(
            """CREATE TABLE IF NOT EXISTS public.categories 
								(
								id serial,
								category_title varchar(256) PRIMARY KEY COLLATE pg_catalog."default"
								)"""
        )

        await postgres_do_query(
            """CREATE TABLE IF NOT EXISTS public.books
								(
								id serial,
								title varchar(256) COLLATE pg_catalog."default",
								author varchar(256) COLLATE pg_catalog."default",
								description varchar(5000) COLLATE pg_catalog."default",
								category varchar(256) COLLATE pg_catalog."default",
								FOREIGN KEY(category) REFERENCES public.categories ON DELETE CASCADE
								)"""
        )

    # --------Table categories---------
    @staticmethod
    async def add_category(title: str):
        try:
            await postgres_do_query(
                "INSERT INTO categories (category_title) VALUES(%s)", (title,)
            )

        except Exception as e:
            logger.exception(f"Ошибка при работа с базой данных: {e}")

    @staticmethod
    async def get_categories():
        try:
            return await postgres_select_all("SELECT * FROM categories")

        except Exception as e:
            logger.exception(f"Ошибка при работа с базой данных: {e}")

    # -------Table books---------
    @staticmethod
    async def add_book(title: str, author: str, description: str, category: str):
        try:
            await postgres_do_query(
                "INSERT INTO books (title, author, description, category) "
                "VALUES(%s, %s, %s, %s)",
                (title, author, description, category),
            )

        except Exception as e:
            logger.exception(f"Ошибка при работа с базой данных: {e}")

    @staticmethod
    async def delete_book(book_id: int):
        try:
            await postgres_do_query("DELETE FROM books WHERE id = %s", (book_id,))

        except Exception as e:
            logger.exception(f"Ошибка при работа с базой данных: {e}")

    @staticmethod
    async def get_all_books():
        try:
            return await postgres_select_all("SELECT * FROM books")

        except Exception as e:
            logger.exception(f"Ошибка при работа с базой данных: {e}")

    @staticmethod
    async def get_book(book_id: int):
        try:
            return await postgres_select_one(
                "SELECT * FROM books WHERE id = %s", (book_id,)
            )

        except Exception as e:
            logger.exception(f"Ошибка при работа с базой данных: {e}")

    @staticmethod
    async def get_books_by_category(category: str):
        try:
            return await postgres_select_all(
                "SELECT * FROM books WHERE category = %s", (category,)
            )

        except Exception as e:
            logger.exception(f"Ошибка при работа с базой данных: {e}")

    @staticmethod
    async def find_book_results(text: str):
        try:
            return await postgres_select_all(
                f"SELECT * FROM books WHERE LOWER(title) LIKE %s OR LOWER(author) LIKE %s",
                (f"%{text}%", f"%{text}%"),
            )

        except Exception as e:
            logger.exception(f"Ошибка при работа с базой данных: {e}")

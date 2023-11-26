from aiogram import executor

from loguru import logger

from loader import dp, bot, bot_commands, db
import handlers

#Функция выполняемая при запсуке бота
async def on_startup(_):
    await db.create_tables()
    await bot.set_my_commands(bot_commands)
    logger.info("Бот запущен!")

#Функция выполняемая при отключении бота
async def on_shutdown(_):
    logger.info("Бот отключен!")


if __name__ == "__main__":
    executor.start_polling(
        dispatcher=dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True
    )

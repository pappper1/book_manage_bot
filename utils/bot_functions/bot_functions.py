# Функция удаления книги
async def delete_book(call, state, db, start_text, ikb):
    await call.answer("")
    book_id = int(call.data.split("delete_book_")[1])
    await state.finish()
    await db.delete_book(book_id=book_id)
    await call.answer(text="🔰 Книга удалена!", show_alert=True)
    await call.message.answer(text=start_text, reply_markup=await ikb.start())
    await call.message.delete()

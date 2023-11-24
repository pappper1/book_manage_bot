import data.keyboards.inline as ikb
from data.media.texts import *

async def back_to_start(call, state):
	await state.finish()

	await call.message.edit_text(text=start_text, reply_markup=await ikb.start())
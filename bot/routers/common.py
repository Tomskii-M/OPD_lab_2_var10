from aiogram import Router, types

from keyboards.common_keyboards import buttons

router = Router(name=__name__)


@router.message()
async def echo_handler(message: types.Message):
    await message.answer(text=f"Неизветсная комнда, воспользуйтесь /help",
                         reply_markup=buttons())
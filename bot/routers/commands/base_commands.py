from aiogram import F, Router, types
from aiogram.filters import Command

from keyboards.common_keyboards import ButtonText, buttons

import Parser

router = Router(name=__name__)


# Хэндлер на команду /start
@router.message(Command("start"))
async def command_start_handler(message: types.Message) -> None:
    await message.answer(text=f"Привет, <b>{message.from_user.full_name}</b>\n\n"
                              "Я бот присылающий <b>курс доллара</b> если он выйдет за "
                              "заданные границы (2 границы верхняя и нижняя).\n\n"
                              "Для просмотра команд /help",
                         reply_markup=buttons())


@router.message(Command("help"))
async def command_help_handler(message: types.Message) -> None:
    await message.answer(text="<b>Привет!</b>\n"
                              "Сначала следует задать границы:\n"
                              "/borders\n\n"
                              "Далее запустить анализ:\n"
                              "/analyse\n"
                              "(/cancel - Для отмены)\n\n"
                              "/dollar - Просмотр текущего курса"
                              "",
                         reply_markup=buttons())


@router.message(F.text == ButtonText.RATE)
@router.message(Command("dollar"))
async def check_dollar(message: types.Message) -> None:
    try:
        await message.answer(text=f"Курс доллара: <b>{Parser.parse()}</b>",
                             reply_markup=buttons())
    except AttributeError:
        await message.answer(text="Не удалось подключиться к серверу...",
                             reply_markup=buttons())

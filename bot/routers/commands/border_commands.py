import asyncio

from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from keyboards.common_keyboards import ButtonText, buttons
from keyboards.inline_keyboards.inline_keyboard import border_cancel

import Parser

router = Router(name=__name__)


class Border(StatesGroup):
    upper = State()  # Ожидание ввода верхней границы
    lower = State()  # Ожидание ввода нижней границы


data = {}  # Словарь пользователя и его границ


@router.message(F.text == ButtonText.BORDERS)
@router.message(Command("borders"))
async def border_upper_handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(Border.upper)
    await message.answer(text="Введите верхнюю границу",
                         reply_markup=border_cancel())


@router.message(Border.upper)
async def border_lower_handler(message: types.Message, state: FSMContext) -> None:
    """Проверка является ли значение числом и запись"""
    try:
        float(message.text)
        await state.update_data(upper=message.text)
        await state.set_state(Border.lower)
        await message.answer(text="Введите нижнюю границу",
                             reply_markup=border_cancel())
    except ValueError:
        await message.answer(text="Вы должны написать число",
                             reply_markup=buttons())
        await state.clear()  # Очистка состояния


@router.message(Border.lower)
async def border_approve(message: types.Message, state: FSMContext) -> None:
    """Проверка является ли значение числом и запись"""
    try:
        float(message.text)
        await state.update_data(lower=message.text)
        data_borders = await state.get_data()
        if float(data_borders["upper"]) > float(data_borders["lower"]):
            data[message.from_user.id] = data_borders
            await message.answer(text=f"Теперь вы можете воспользоваться /analyse",
                                 reply_markup=buttons())
        else:
            await message.answer(text=f"Неправильно заданы границы. Попробуйте ещё раз /borders",
                                 reply_markup=buttons())

    except ValueError:
        await message.answer(text="Вы должны написать число",
                             reply_markup=buttons())

    await state.clear()  # Очистка состояния


@router.callback_query(F.data == "border_cancel")
async def callback_query_cancel(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()  # Очистка состояния
    await call.answer(text="Отправка отменена")
    await call.message.delete()
    await call.message.answer(text="Отправка отменена",
                              reply_markup=buttons())


@router.message(F.text == ButtonText.ANALYSE)
@router.message(Command("analyse"))
async def command_analyse_handler(message: types.Message) -> None:
    if message.from_user.id in data:
        await message.answer(text="Анализ запущен...",
                             reply_markup=buttons())
        try:
            # Запуск цикла, пока курс не выйдет за заданные границу
            while (float(data[message.from_user.id]["lower"]) < Parser.parse()
                   < float(data[message.from_user.id]["upper"])):
                await asyncio.sleep(30)
            else:
                if Parser.parse() < float(data[message.from_user.id]["lower"]):
                    await message.answer(text="Курс пробил нижнюю границу /dollar",
                                         reply_markup=buttons())
                elif Parser.parse() > float(data[message.from_user.id]["upper"]):
                    await message.answer(text="Курс пробил верхнюю границу /dollar",
                                         reply_markup=buttons())
                del data[message.from_user.id]
        except AttributeError:
            await message.answer(text="Не удалось подключиться к серверу...",
                                 reply_markup=buttons())
        # Пользователь ввёл команду cancel
        except KeyError:
            pass

    else:
        await message.answer(text="Сначала введите границы /borders")


@router.message(F.text == ButtonText.CANCEL)
@router.message(Command("cancel"))
async def command_cancel_handler(message: types.Message) -> None:
    try:
        del data[message.from_user.id]
        await message.answer(text="Анализ принудительно завершён",
                             reply_markup=buttons())
    except KeyError:
        await message.answer(text="Анализ не запущен /analyse",
                             reply_markup=buttons())

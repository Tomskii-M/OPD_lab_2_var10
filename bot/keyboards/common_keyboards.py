from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


class ButtonText:
    BORDERS = "🔺Ввести границы🔻"
    ANALYSE = "🔔Запустить анализ"
    RATE = "💰Курс доллара"
    CANCEL = "❌ОТМЕНИТЬ"


def buttons():
    button_borders = KeyboardButton(text=ButtonText.BORDERS)
    button_analyse = KeyboardButton(text=ButtonText.ANALYSE)
    button_rate = KeyboardButton(text=ButtonText.RATE)
    button_cancel = KeyboardButton(text=ButtonText.CANCEL)
    buttons_first_row = [button_borders, button_analyse]
    buttons_second_row = [button_rate, button_cancel]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_first_row, buttons_second_row]
    )
    return markup

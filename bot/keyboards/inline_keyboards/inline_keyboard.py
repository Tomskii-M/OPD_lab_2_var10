from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class InlineText:
    CANCEL = "ОТМЕНИТЬ"


def border_cancel():
    button_cancel = InlineKeyboardButton(text=InlineText.CANCEL, callback_data="border_cancel")
    buttons_first_row = [button_cancel]
    markup = InlineKeyboardMarkup(
        inline_keyboard=[buttons_first_row]
    )
    return markup

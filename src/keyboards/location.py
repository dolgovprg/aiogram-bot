from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def locations_keyboard(locations: list):
    """
    Функція для створення клавіатури для вибору локації
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    for item in locations:
        keyboard.insert(InlineKeyboardButton(item, callback_data=item))
    return keyboard
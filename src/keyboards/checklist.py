from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def checklist_keyboard():
    """
    Функція для створення клавіатури для вибору пункту чек-листа
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Все чисто", callback_data="ok"),
        InlineKeyboardButton(text="Ввести комментар", callback_data="Commment"),
    )
    return keyboard
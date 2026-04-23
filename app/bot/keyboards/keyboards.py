from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_lang_settings_kb() -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(
        text='English',
        callback_data='English'
    )
    button_2 = InlineKeyboardButton(
        text='Russian',
        callback_data='Russian'
    )
    button_3 = InlineKeyboardButton(
        text='Cancel',
        callback_data='cancel_new_user_settings'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1, button_2],[button_3]]
    )
    return keyboard

def get_timezone_settings_kb() -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(
        text='Cancel',
        callback_data='cancel_new_user_settings'
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button_1]]
    )
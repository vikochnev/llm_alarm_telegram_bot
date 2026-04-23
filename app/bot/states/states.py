from aiogram.fsm.state import State, StatesGroup

class UserSettingsState(StatesGroup):
    fill_lang = State()
    fill_timezone = State()

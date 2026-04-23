from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import BotCommandScopeChat, CallbackQuery, Message
from app.bot.filters.filters import UserInDBFilter
from app.bot.keyboards.keyboards import get_lang_settings_kb, get_timezone_settings_kb
from app.bot.states.states import UserSettingsState
from app.bot.llm.llm_queries import get_timezone_llm_response

import logging

logger = logging.getLogger(__name__)

user_settings_router = Router()

@user_settings_router.callback_query(F.data=='cancel_settings')
async def process_cancel_button_click(
        callback_query: CallbackQuery,
        state: FSMContext,
):
    await callback_query.answer(
        text='Cancelling setting up user'
    )
    await state.set_state(default_state)

@user_settings_router.message(~UserInDBFilter(), CommandStart())
async def process_start_new_user_registration(
        message: Message,
        state: FSMContext,
):
    await message.answer(
        text="Enter your preferred language",
        reply_markup=get_lang_settings_kb(),
    )
    await state.set_state(UserSettingsState.fill_lang)

@user_settings_router.callback_query(~UserInDBFilter(),
    StateFilter(UserSettingsState.fill_lang),
    F.data.in_(['English', 'Russian'])
)
async def process_user_setting_language(
        callback: CallbackQuery,
        state: FSMContext,
):
    await state.update_data(lang=callback.data)
    await callback.message.delete()
    await callback.answer(
        text="Enter your timezone or city name",
        reply_markup=get_timezone_settings_kb(),
    )
    await state.set_state(UserSettingsState.fill_timezone)

@user_settings_router.message(
    ~UserInDBFilter(),
    StateFilter(UserSettingsState.fill_timezone),
)
async def process_user_setting_timezone(
        message: Message,
        state: FSMContext,
):
    llm_response = await get_timezone_llm_response(user_input=message.text)
    if llm_response == 'invalid':
        await message.answer(
            text="Incorrect input."
                 "Enter your timezone or city name",
        )
    else:
        await state.update_data(timezone=llm_response)
        await state.set_state(default_state)
        await message.answer(
            text=f"Timezone set to {llm_response}",
        )


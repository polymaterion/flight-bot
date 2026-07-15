from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.db import database as db
from bot.keyboards.main_menu import main_menu_kb, settings_kb
from bot.locales.texts import TEXTS, t

router = Router(name="settings")


def _is_settings_button(message: Message) -> bool:
    return message.text in (TEXTS["menu_settings"]["ru"], TEXTS["menu_settings"]["tk"])


@router.message(_is_settings_button)
async def show_settings(message: Message) -> None:
    lang = await db.get_user_lang(message.from_user.id)
    await message.answer(t("settings_menu", lang), reply_markup=settings_kb(lang))


@router.callback_query(F.data.startswith("setlang:"))
async def change_language(callback: CallbackQuery) -> None:
    new_lang = callback.data.split(":", 1)[1]
    if new_lang not in ("ru", "tk"):
        new_lang = "ru"

    await db.set_user_lang(callback.from_user.id, new_lang)

    await callback.message.edit_text(t("language_set", new_lang))
    await callback.message.answer(
        t("welcome", new_lang),
        reply_markup=main_menu_kb(new_lang),
    )
    await callback.answer()

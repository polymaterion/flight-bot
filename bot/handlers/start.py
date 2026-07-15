from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from bot.db import database as db
from bot.keyboards.main_menu import language_choice_kb, main_menu_kb
from bot.locales.texts import t

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await db.upsert_user(message.from_user.id, lang="ru")
    await message.answer(
        t("choose_language", "ru"),
        reply_markup=language_choice_kb(),
    )


@router.callback_query(F.data.startswith("lang:"))
async def on_language_chosen(callback: CallbackQuery) -> None:
    lang = callback.data.split(":", 1)[1]
    if lang not in ("ru", "tk"):
        lang = "ru"

    await db.set_user_lang(callback.from_user.id, lang)

    await callback.message.edit_text(t("language_set", lang))
    await callback.message.answer(
        t("welcome", lang),
        reply_markup=main_menu_kb(lang),
    )
    await callback.answer()

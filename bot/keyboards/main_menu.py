from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from bot.locales.texts import t


def language_choice_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
                InlineKeyboardButton(text="🇹🇲 Türkmençe", callback_data="lang:tk"),
            ]
        ]
    )


def main_menu_kb(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("menu_search", lang))],
            [KeyboardButton(text=t("menu_subs", lang)), KeyboardButton(text=t("menu_settings", lang))],
        ],
        resize_keyboard=True,
    )


def settings_kb(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_lang_ru", lang), callback_data="setlang:ru"),
                InlineKeyboardButton(text=t("btn_lang_tk", lang), callback_data="setlang:tk"),
            ]
        ]
    )

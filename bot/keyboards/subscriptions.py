from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.data.cities import city_label
from bot.locales.texts import t


def subscription_item_kb(lang: str, sub_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("btn_delete_sub", lang), callback_data=f"sub_del:{sub_id}")]
        ]
    )

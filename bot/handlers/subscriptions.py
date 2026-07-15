from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.data.cities import city_label
from bot.db import database as db
from bot.keyboards.subscriptions import subscription_item_kb
from bot.locales.texts import TEXTS, t

router = Router(name="subscriptions")


def _is_subs_button(message: Message) -> bool:
    return message.text in (TEXTS["menu_subs"]["ru"], TEXTS["menu_subs"]["tk"])


@router.message(_is_subs_button)
async def show_subscriptions(message: Message) -> None:
    lang = await db.get_user_lang(message.from_user.id)
    subs = await db.get_user_subscriptions(message.from_user.id)

    if not subs:
        await message.answer(t("subs_empty", lang))
        return

    await message.answer(t("subs_header", lang))

    for i, sub in enumerate(subs, start=1):
        price_label = (
            f"{int(sub['last_price'])} {sub['last_currency']}"
            if sub["last_price"] is not None
            else t("sub_no_price_yet", lang)
        )
        text = t(
            "sub_item",
            lang,
            i=i,
            origin=city_label(sub["origin"], lang),
            destination=city_label(sub["destination"], lang),
            price=price_label,
        )
        await message.answer(text, reply_markup=subscription_item_kb(lang, sub["id"]))


@router.callback_query(F.data.startswith("sub_del:"))
async def delete_subscription(callback: CallbackQuery) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    sub_id = int(callback.data.split(":", 1)[1])

    await db.delete_subscription(sub_id, callback.from_user.id)

    await callback.message.edit_text(t("sub_deleted", lang))
    await callback.answer()

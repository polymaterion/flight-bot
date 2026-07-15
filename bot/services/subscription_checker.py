"""
Фоновая задача: периодически проверяет цены по всем подпискам
и уведомляет пользователей, если появилась новая цена или цена снизилась.
"""

import logging

from aiogram import Bot

from bot.data.cities import city_label
from bot.db import database as db
from bot.locales.texts import t
from bot.services.travelpayouts import TravelpayoutsClient
from bot.utils.dates import format_date_human
from datetime import date as date_cls

logger = logging.getLogger(__name__)


async def check_all_subscriptions(bot: Bot, tp_client: TravelpayoutsClient) -> None:
    subs = await db.get_all_subscriptions()
    logger.info("Проверка %d подписок", len(subs))

    for sub in subs:
        try:
            await _check_one(bot, tp_client, sub)
        except Exception:
            logger.exception("Ошибка при проверке подписки id=%s", sub["id"])


async def _check_one(bot: Bot, tp_client: TravelpayoutsClient, sub) -> None:
    depart_date = sub["depart_date"]  # может быть None
    options = await tp_client.find_prices(
        origin=sub["origin"],
        destination=sub["destination"],
        depart_date=depart_date if isinstance(depart_date, date_cls) else None,
    )

    if not options:
        return

    best = options[0]
    old_price = float(sub["last_price"]) if sub["last_price"] is not None else None

    is_new_price = old_price is None
    is_price_drop = old_price is not None and best.price < old_price

    if not (is_new_price or is_price_drop):
        return

    await db.update_subscription_price(sub["id"], best.price, best.currency)

    lang = sub["lang"] or "ru"
    depart_label = (
        format_date_human(date_cls.fromisoformat(best.depart_date), lang)
        if best.depart_date
        else "-"
    )

    text = t(
        "price_drop_alert",
        lang,
        origin=city_label(sub["origin"], lang),
        destination=city_label(sub["destination"], lang),
        date=depart_label,
        price=int(best.price),
        currency=best.currency,
    )

    try:
        await bot.send_message(sub["user_id"], text)
    except Exception:
        logger.exception("Не удалось отправить уведомление user_id=%s", sub["user_id"])

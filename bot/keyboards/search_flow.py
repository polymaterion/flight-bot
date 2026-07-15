from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.data.cities import City, destination_choices, origin_choices
from bot.locales.texts import t


def _chunk(items: list, size: int = 2) -> list[list]:
    return [items[i:i + size] for i in range(0, len(items), size)]


def origin_kb(lang: str) -> InlineKeyboardMarkup:
    cities = origin_choices()
    buttons = [
        InlineKeyboardButton(
            text=(city.name_tk if lang == "tk" else city.name_ru) + f" {city.flag}",
            callback_data=f"origin:{city.code}",
        )
        for city in cities
    ]
    rows = _chunk(buttons, 2)
    rows.append([InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="search:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def destination_kb(lang: str, origin_code: str) -> InlineKeyboardMarkup:
    cities: list[City] = destination_choices(origin_code)
    buttons = [
        InlineKeyboardButton(
            text=(city.name_tk if lang == "tk" else city.name_ru) + f" {city.flag}",
            callback_data=f"dest:{city.code}",
        )
        for city in cities
    ]
    rows = _chunk(buttons, 2)
    rows.append([InlineKeyboardButton(text=t("btn_back", lang), callback_data="search:back_to_origin")])
    rows.append([InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="search:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def date_choice_kb(lang: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=t("btn_this_month", lang), callback_data="date:this_month")],
        [InlineKeyboardButton(text=t("btn_next_month", lang), callback_data="date:next_month")],
        [InlineKeyboardButton(text=t("btn_pick_date", lang), callback_data="date:pick")],
        [InlineKeyboardButton(text=t("btn_pick_range", lang), callback_data="date:range")],
        [InlineKeyboardButton(text=t("btn_back", lang), callback_data="search:back_to_destination")],
        [InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="search:cancel")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def route_preview_kb(lang: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=t("btn_confirm", lang), callback_data="preview:confirm")],
        [InlineKeyboardButton(text=t("btn_change", lang), callback_data="preview:change")],
        [InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="search:cancel")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def no_results_kb(lang: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=t("btn_subscribe", lang), callback_data="results:subscribe")],
        [InlineKeyboardButton(text=t("btn_new_search", lang), callback_data="results:new_search")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


def flight_card_kb(lang: str, buy_link: str, offer_subscribe: bool = True) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=t("btn_buy", lang), url=buy_link)]]
    if offer_subscribe:
        rows.append(
            [InlineKeyboardButton(text=t("btn_subscribe", lang), callback_data="results:subscribe")]
        )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def after_results_kb(lang: str) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=t("btn_new_search", lang), callback_data="results:new_search")]]
    return InlineKeyboardMarkup(inline_keyboard=rows)

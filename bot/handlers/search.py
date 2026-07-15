from datetime import date

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.data.cities import city_label, get_city
from bot.db import database as db
from bot.handlers.states import SearchFlow
from bot.keyboards.main_menu import main_menu_kb
from bot.keyboards.search_flow import (
    date_choice_kb,
    destination_kb,
    flight_card_kb,
    no_results_kb,
    origin_kb,
    route_preview_kb,
)
from bot.locales.texts import TEXTS, t
from bot.services.travelpayouts import TravelpayoutsClient
from bot.utils.dates import (
    first_day_of_next_month,
    first_day_of_this_month,
    format_date_human,
    is_in_past,
    parse_date_ddmmyyyy,
    parse_date_range,
)

router = Router(name="search")

# Клиент Travelpayouts прокидывается из main.py через router["tp_client"]
# (см. bot/main.py -> router.search.tp_client = ...)
tp_client: TravelpayoutsClient | None = None


def _is_search_button(message: Message) -> bool:
    return message.text in (TEXTS["menu_search"]["ru"], TEXTS["menu_search"]["tk"])


# ---------- Шаг 1: старт флоу, выбор города вылета ----------

@router.message(_is_search_button)
async def start_search(message: Message, state: FSMContext) -> None:
    lang = await db.get_user_lang(message.from_user.id)
    await state.clear()
    await state.set_state(SearchFlow.choosing_origin)
    await message.answer(t("choose_origin", lang), reply_markup=origin_kb(lang))


@router.callback_query(F.data == "search:cancel")
async def cancel_search(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    await state.clear()
    await callback.message.edit_text(t("action_cancelled", lang))
    await callback.message.answer(t("welcome", lang), reply_markup=main_menu_kb(lang))
    await callback.answer()


# ---------- Шаг 2: выбор города вылета -> показать города назначения ----------

@router.callback_query(SearchFlow.choosing_origin, F.data.startswith("origin:"))
async def on_origin_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    origin_code = callback.data.split(":", 1)[1]

    await state.update_data(origin=origin_code)
    await state.set_state(SearchFlow.choosing_destination)

    await callback.message.edit_text(
        t("choose_destination", lang),
        reply_markup=destination_kb(lang, origin_code),
    )
    await callback.answer()


@router.callback_query(F.data == "search:back_to_origin")
async def back_to_origin(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    await state.set_state(SearchFlow.choosing_origin)
    await callback.message.edit_text(t("choose_origin", lang), reply_markup=origin_kb(lang))
    await callback.answer()


# ---------- Шаг 3: выбор города назначения -> выбор даты ----------

@router.callback_query(SearchFlow.choosing_destination, F.data.startswith("dest:"))
async def on_destination_chosen(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    data = await state.get_data()
    origin_code = data["origin"]
    destination_code = callback.data.split(":", 1)[1]

    if origin_code == destination_code:
        await callback.answer(t("same_city_error", lang), show_alert=True)
        return

    await state.update_data(destination=destination_code)
    await state.set_state(SearchFlow.choosing_date)

    await callback.message.edit_text(t("choose_date", lang), reply_markup=date_choice_kb(lang))
    await callback.answer()


@router.callback_query(F.data == "search:back_to_destination")
async def back_to_destination(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    data = await state.get_data()
    origin_code = data["origin"]
    await state.set_state(SearchFlow.choosing_destination)
    await callback.message.edit_text(
        t("choose_destination", lang),
        reply_markup=destination_kb(lang, origin_code),
    )
    await callback.answer()


# ---------- Шаг 4: выбор даты ----------

@router.callback_query(SearchFlow.choosing_date, F.data == "date:this_month")
async def date_this_month(callback: CallbackQuery, state: FSMContext) -> None:
    await _set_single_date_and_preview(callback, state, first_day_of_this_month())


@router.callback_query(SearchFlow.choosing_date, F.data == "date:next_month")
async def date_next_month(callback: CallbackQuery, state: FSMContext) -> None:
    await _set_single_date_and_preview(callback, state, first_day_of_next_month())


@router.callback_query(SearchFlow.choosing_date, F.data == "date:pick")
async def date_pick_manual(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    await state.set_state(SearchFlow.entering_date_manual)
    await callback.message.edit_text(t("enter_date_manual", lang))
    await callback.answer()


@router.callback_query(SearchFlow.choosing_date, F.data == "date:range")
async def date_pick_range(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    await state.set_state(SearchFlow.entering_date_range)
    await callback.message.edit_text(t("enter_date_range_manual", lang))
    await callback.answer()


@router.message(SearchFlow.entering_date_manual)
async def on_manual_date_entered(message: Message, state: FSMContext) -> None:
    lang = await db.get_user_lang(message.from_user.id)
    parsed = parse_date_ddmmyyyy(message.text or "")

    if parsed is None:
        await message.answer(t("invalid_date", lang))
        return
    if is_in_past(parsed):
        await message.answer(t("date_in_past", lang))
        return

    await state.update_data(depart_date=parsed.isoformat(), return_date=None)
    await _show_preview(message, state, lang)


@router.message(SearchFlow.entering_date_range)
async def on_range_entered(message: Message, state: FSMContext) -> None:
    lang = await db.get_user_lang(message.from_user.id)
    parsed = parse_date_range(message.text or "")

    if parsed is None:
        await message.answer(t("invalid_date", lang))
        return

    start, end = parsed
    if is_in_past(start):
        await message.answer(t("date_in_past", lang))
        return

    await state.update_data(depart_date=start.isoformat(), return_date=end.isoformat())
    await _show_preview(message, state, lang)


async def _set_single_date_and_preview(
    callback: CallbackQuery, state: FSMContext, d: date
) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    await state.update_data(depart_date=d.isoformat(), return_date=None)
    await _show_preview(callback.message, state, lang, edit=True)
    await callback.answer()


# ---------- Шаг 5: превью маршрута ----------

async def _show_preview(
    message: Message, state: FSMContext, lang: str, edit: bool = False
) -> None:
    data = await state.get_data()
    origin_code = data["origin"]
    destination_code = data["destination"]
    depart_date = date.fromisoformat(data["depart_date"])
    return_date_str = data.get("return_date")

    date_label = format_date_human(depart_date, lang)
    if return_date_str:
        return_date = date.fromisoformat(return_date_str)
        date_label += f" — {format_date_human(return_date, lang)}"

    text = t(
        "route_preview",
        lang,
        origin=city_label(origin_code, lang),
        destination=city_label(destination_code, lang),
        date=date_label,
    )

    await state.set_state(SearchFlow.previewing)

    if edit:
        await message.edit_text(text, reply_markup=route_preview_kb(lang))
    else:
        await message.answer(text, reply_markup=route_preview_kb(lang))


@router.callback_query(SearchFlow.previewing, F.data == "preview:change")
async def preview_change(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    await state.set_state(SearchFlow.choosing_origin)
    await callback.message.edit_text(t("choose_origin", lang), reply_markup=origin_kb(lang))
    await callback.answer()


@router.callback_query(SearchFlow.previewing, F.data == "preview:confirm")
async def preview_confirm(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    data = await state.get_data()
    origin_code = data["origin"]
    destination_code = data["destination"]
    depart_date = date.fromisoformat(data["depart_date"])

    await callback.message.edit_text(t("searching", lang))
    await callback.answer()

    assert tp_client is not None, "TravelpayoutsClient не инициализирован"

    try:
        options = await tp_client.find_prices(
            origin=origin_code, destination=destination_code, depart_date=depart_date
        )
    except Exception:
        options = []

    if not options:
        await callback.message.answer(t("no_results", lang), reply_markup=no_results_kb(lang))
        # оставляем данные о маршруте в state - вдруг пользователь нажмёт "подписаться"
        return

    await callback.message.answer(t("search_results_header", lang))

    for option in options:
        transfers = (
            t("transfers_direct", lang)
            if option.number_of_changes == 0
            else t("transfers_n", lang, n=option.number_of_changes)
        )
        depart_label = (
            format_date_human(date.fromisoformat(option.depart_date), lang)
            if option.depart_date
            else "-"
        )
        card_text = t(
            "flight_card",
            lang,
            origin=city_label(origin_code, lang),
            destination=city_label(destination_code, lang),
            date=depart_label,
            transfers=transfers,
            price=int(option.price),
            currency=option.currency,
        )
        await callback.message.answer(
            card_text, reply_markup=flight_card_kb(lang, option.link)
        )

    await callback.message.answer(
        t("btn_new_search", lang),
        reply_markup=main_menu_kb(lang),
    )
    await state.clear()


# ---------- Подписка из экрана "нет результатов" или из карточки ----------

@router.callback_query(F.data == "results:subscribe")
async def subscribe_to_route(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    data = await state.get_data()
    origin_code = data.get("origin")
    destination_code = data.get("destination")
    depart_date_str = data.get("depart_date")

    if not origin_code or not destination_code:
        await callback.answer(t("generic_error", lang), show_alert=True)
        return

    depart_date = date.fromisoformat(depart_date_str) if depart_date_str else None

    await db.add_subscription(
        user_id=callback.from_user.id,
        origin=origin_code,
        destination=destination_code,
        depart_date=depart_date,
    )

    await callback.message.answer(
        t(
            "subscribed_ok",
            lang,
            origin=city_label(origin_code, lang),
            destination=city_label(destination_code, lang),
        ),
        reply_markup=main_menu_kb(lang),
    )
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == "results:new_search")
async def new_search_from_results(callback: CallbackQuery, state: FSMContext) -> None:
    lang = await db.get_user_lang(callback.from_user.id)
    await state.clear()
    await state.set_state(SearchFlow.choosing_origin)
    await callback.message.answer(t("choose_origin", lang), reply_markup=origin_kb(lang))
    await callback.answer()

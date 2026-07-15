"""
Интеграция с Aviasales Data API (Travelpayouts).

ВАЖНО: полноценный real-time Flight Search API у Travelpayouts выдаётся
только проектам с подтверждённым MAU >= 50 000. Для нового бота это
недоступно, поэтому здесь используется открытый всем Data API
(v3/get_latest_prices и v1/prices/calendar), который отдаёт цены из
кэша по реальным поискам других пользователей Aviasales за последние
48 часов - 7 дней. Это не "живой" поиск, а хорошая оценка цены плюс
ссылка на реальную покупку - переход происходит на сайт Aviasales,
где уже показываются актуальные варианты.

Документация:
https://support.travelpayouts.com/hc/en-us/articles/203956163
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional

import aiohttp

BASE_URL = "https://api.travelpayouts.com"


@dataclass
class PriceOption:
    origin: str
    destination: str
    depart_date: Optional[str]
    return_date: Optional[str]
    price: float
    currency: str
    number_of_changes: int
    link: str


class TravelpayoutsClient:
    def __init__(self, token: str, marker: str):
        self._token = token
        self._marker = marker

    async def _get(self, path: str, params: dict) -> dict:
        headers = {"x-access-token": self._token}
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{BASE_URL}{path}", params=params, headers=headers, timeout=15
            ) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def find_prices(
        self,
        origin: str,
        destination: str,
        depart_date: Optional[date] = None,
        currency: str = "rub",
    ) -> list[PriceOption]:
        """
        Ищет известные цены по направлению через v3/get_latest_prices.
        Если depart_date указана - дополнительно фильтруем результат по месяцу вылета,
        так как API этого метода принимает только период (month/year), а не точную дату.
        """
        params = {
            "origin": origin,
            "destination": destination,
            "currency": currency,
            "period_type": "month",
            "show_to_affiliates": "true",
            "sorting": "price",
            "token": self._token,
        }
        if depart_date is not None:
            params["month"] = depart_date.strftime("%Y-%m-01")

        data = await self._get("/aviasales/v3/get_latest_prices", params)
        raw_items = data.get("data", []) if data.get("success") else []

        results: list[PriceOption] = []
        for item in raw_items:
            item_depart = item.get("depart_date")
            if depart_date is not None and item_depart:
                if not item_depart.startswith(depart_date.strftime("%Y-%m")):
                    continue
            results.append(
                PriceOption(
                    origin=item.get("origin", origin),
                    destination=item.get("destination", destination),
                    depart_date=item_depart,
                    return_date=item.get("return_date") or None,
                    price=float(item.get("value", 0)),
                    currency=currency.upper(),
                    number_of_changes=int(item.get("number_of_changes", 0)),
                    link=self.build_search_link(
                        origin, destination, item_depart, item.get("return_date")
                    ),
                )
            )

        results.sort(key=lambda x: x.price)
        return results[:5]

    def build_search_link(
        self,
        origin: str,
        destination: str,
        depart_date: Optional[str],
        return_date: Optional[str] = None,
    ) -> str:
        """
        Формирует диплинк на поиск Aviasales с partner marker.
        Формат даты для Aviasales: DDMM (например 2508).
        """
        date_part = ""
        if depart_date:
            y, m, d = depart_date.split("-")
            date_part = f"{d}{m}"
            if return_date:
                ry, rm, rd = return_date.split("-")
                date_part += f"{rd}{rm}"

        route = f"{origin}{date_part}{destination}1"
        return (
            f"https://www.aviasales.com/search/{route}"
            f"?marker={self._marker}"
        )

    def build_generic_search_link(self, origin: str, destination: str) -> str:
        """Ссылка без даты - на случай, если данных по конкретной дате нет совсем."""
        route = f"{origin}{destination}1"
        return f"https://www.aviasales.com/search/{route}?marker={self._marker}"

"""
Справочник городов/аэропортов для бота.

Логика направлений:
- TKM города (is_tkm=True) можно выбрать и как "откуда", и как "куда".
- Не-TKM города (Россия/Беларусь) можно выбрать только как "откуда" -
  из них турист улетает в Туркменистан, обратных внутренних маршрутов не бывает.
- Если "откуда" = не-TKM город -> список "куда" содержит только TKM города.
- Если "откуда" = TKM город -> список "куда" содержит ВСЕ города (TKM + не-TKM),
  кроме самого города вылета - это покрывает и внутренние рейсы, и вылет обратно в РФ/Беларусь.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class City:
    code: str  # IATA код (город или аэропорт)
    name_ru: str
    name_tk: str
    flag: str
    is_tkm: bool


CITIES: dict[str, City] = {
    # --- Туркменистан ---
    "ASB": City("ASB", "Ашхабад", "Aşgabat", "🇹🇲", True),
    "CRZ": City("CRZ", "Туркменабат", "Türkmenabat", "🇹🇲", True),
    "MYP": City("MYP", "Мары", "Mary", "🇹🇲", True),
    "TAZ": City("TAZ", "Дашогуз", "Daşoguz", "🇹🇲", True),
    "KRW": City("KRW", "Туркменбаши", "Türkmenbaşy", "🇹🇲", True),
    "BKN": City("BKN", "Балканабат", "Balkanabat", "🇹🇲", True),

    # --- Города вылета (СНГ) ---
    "MOW": City("MOW", "Москва", "Moskwa", "🇷🇺", False),
    "LED": City("LED", "Санкт-Петербург", "Sankt-Peterburg", "🇷🇺", False),
    "KZN": City("KZN", "Казань", "Kazan", "🇷🇺", False),
    "MSQ": City("MSQ", "Минск", "Minsk", "🇧🇾", False),
    "SVX": City("SVX", "Екатеринбург", "Ekaterinburg", "🇷🇺", False),
    "KUF": City("KUF", "Самара", "Samara", "🇷🇺", False),
    "OVB": City("OVB", "Новосибирск", "Nowosibirsk", "🇷🇺", False),
}

# Порядок отображения кнопок "откуда"
ORIGIN_ORDER = ["MOW", "LED", "KZN", "MSQ", "SVX", "KUF", "OVB",
                 "ASB", "CRZ", "MYP", "TAZ", "KRW", "BKN"]

# Порядок отображения кнопок "куда", когда доступны только города ТКМ
TKM_ORDER = ["ASB", "CRZ", "MYP", "TAZ", "KRW", "BKN"]

# Полный порядок (используется, когда "откуда" - город ТКМ)
ALL_ORDER = ["ASB", "CRZ", "MYP", "TAZ", "KRW", "BKN",
             "MOW", "LED", "KZN", "MSQ", "SVX", "KUF", "OVB"]


def get_city(code: str) -> City | None:
    return CITIES.get(code.upper())


def city_label(code: str, lang: str) -> str:
    c = get_city(code)
    if not c:
        return code
    name = c.name_tk if lang == "tk" else c.name_ru
    return f"{c.flag} {name}"


def origin_choices() -> list[City]:
    return [CITIES[code] for code in ORIGIN_ORDER]


def destination_choices(origin_code: str) -> list[City]:
    """Возвращает доступные города назначения в зависимости от города вылета."""
    origin = get_city(origin_code)
    if origin is None:
        return []

    if origin.is_tkm:
        # из ТКМ можно улететь куда угодно (внутренние рейсы + обратно в СНГ),
        # кроме самого города вылета
        return [CITIES[code] for code in ALL_ORDER if code != origin_code]
    else:
        # из СНГ - только в Туркменистан
        return [CITIES[code] for code in TKM_ORDER]

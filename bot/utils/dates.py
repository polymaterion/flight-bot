from datetime import date, datetime, timedelta


def first_day_of_this_month() -> date:
    today = date.today()
    return today.replace(day=1)


def first_day_of_next_month() -> date:
    today = date.today()
    if today.month == 12:
        return date(today.year + 1, 1, 1)
    return date(today.year, today.month + 1, 1)


def parse_date_ddmmyyyy(text: str) -> date | None:
    text = text.strip()
    try:
        parsed = datetime.strptime(text, "%d.%m.%Y").date()
        return parsed
    except ValueError:
        return None


def parse_date_range(text: str) -> tuple[date, date] | None:
    """Ожидаемый формат: 20.08.2026-31.08.2026"""
    text = text.strip()
    parts = text.split("-")
    if len(parts) != 2:
        return None
    start = parse_date_ddmmyyyy(parts[0])
    end = parse_date_ddmmyyyy(parts[1])
    if start is None or end is None:
        return None
    if end < start:
        start, end = end, start
    return start, end


def format_date_human(d: date, lang: str) -> str:
    months_ru = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря",
    ]
    months_tk = [
        "ýanwar", "fewral", "mart", "aprel", "maý", "iýun",
        "iýul", "awgust", "sentýabr", "oktýabr", "noýabr", "dekabr",
    ]
    months = months_tk if lang == "tk" else months_ru
    return f"{d.day} {months[d.month - 1]} {d.year}"


def is_in_past(d: date) -> bool:
    return d < date.today()

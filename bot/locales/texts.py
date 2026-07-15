"""
Все текстовые строки бота на двух языках.
Использование: t("key", lang, **kwargs)
"""

TEXTS: dict[str, dict[str, str]] = {
    "choose_language": {
        "ru": "🌐 Выберите язык / Diliňizi saýlaň",
        "tk": "🌐 Выберите язык / Diliňizi saýlaň",
    },
    "language_set": {
        "ru": "Язык установлен: Русский ✅",
        "tk": "Dil saýlandy: Türkmen ✅",
    },
    "welcome": {
        "ru": (
            "👋 Salam! Это бот поиска авиабилетов в Туркменистан и обратно.\n\n"
            "✈️ Найти билеты — подобрать рейс по датам и направлению\n"
            "🔔 Мои подписки — следить за ценой на нужный рейс\n"
            "⚙️ Настройки — сменить язык\n\n"
            "Выберите действие на клавиатуре ниже 👇"
        ),
        "tk": (
            "👋 Salam! Bu bot Türkmenistana we yzyna uçuş biletlerini gözlemek üçin.\n\n"
            "✈️ Bilet gözle — ugur we senä görä uçuş saýlamak\n"
            "🔔 Yzarlamalarym — gerekli uçuşyň bahasyny yzarlamak\n"
            "⚙️ Sazlamalar — dili üýtgetmek\n\n"
            "Aşakdaky klawiaturadan hereket saýlaň 👇"
        ),
    },
    "menu_search": {"ru": "✈️ Найти билеты", "tk": "✈️ Bilet gözle"},
    "menu_subs": {"ru": "🔔 Мои подписки", "tk": "🔔 Yzarlamalarym"},
    "menu_settings": {"ru": "⚙️ Настройки", "tk": "⚙️ Sazlamalar"},

    "choose_origin": {
        "ru": "🛫 Откуда летим?",
        "tk": "🛫 Nireden uçjak?",
    },
    "choose_destination": {
        "ru": "🛬 Куда летим?",
        "tk": "🛬 Nirä uçjak?",
    },
    "choose_date": {
        "ru": "📅 Когда хотите лететь?",
        "tk": "📅 Haçan uçmak isleýärsiňiz?",
    },
    "btn_this_month": {"ru": "Этот месяц", "tk": "Bu aý"},
    "btn_next_month": {"ru": "Следующий месяц", "tk": "Indiki aý"},
    "btn_pick_date": {"ru": "📆 Указать дату", "tk": "📆 Senäni görkez"},
    "btn_pick_range": {"ru": "📆 Указать диапазон дат", "tk": "📆 Sene aralygyny görkez"},
    "btn_back": {"ru": "◀️ Назад", "tk": "◀️ Yza"},
    "btn_cancel": {"ru": "✖️ Отменить", "tk": "✖️ Ýatyr"},
    "btn_confirm": {"ru": "✅ Подтвердить", "tk": "✅ Tassykla"},
    "btn_change": {"ru": "✏️ Изменить", "tk": "✏️ Üýtget"},

    "enter_date_manual": {
        "ru": "Введите дату вылета в формате ДД.ММ.ГГГГ, например 25.08.2026",
        "tk": "Uçuş senesini ГГГГ.АА.ГГ görnüşinde ýazyň, mysal üçin 25.08.2026",
    },
    "enter_date_range_manual": {
        "ru": (
            "Введите диапазон дат в формате ДД.ММ.ГГГГ-ДД.ММ.ГГГГ\n"
            "Например: 20.08.2026-31.08.2026"
        ),
        "tk": (
            "Sene aralygyny ГГГГ.АА.ГГ-ГГГГ.АА.ГГ görnüşinde ýazyň\n"
            "Mysal: 20.08.2026-31.08.2026"
        ),
    },
    "invalid_date": {
        "ru": "⚠️ Не получилось распознать дату. Попробуйте ещё раз, формат: ДД.ММ.ГГГГ",
        "tk": "⚠️ Sene tanalmady. Ýene synanyşyň, format: ГГГГ.АА.ГГ",
    },
    "date_in_past": {
        "ru": "⚠️ Эта дата уже прошла. Укажите дату в будущем.",
        "tk": "⚠️ Bu sene eýýäm geçdi. Geljekki senäni görkeziň.",
    },

    "route_preview": {
        "ru": (
            "🧾 Проверьте маршрут:\n\n"
            "🛫 Откуда: {origin}\n"
            "🛬 Куда: {destination}\n"
            "📅 Дата: {date}\n\n"
            "Всё верно?"
        ),
        "tk": (
            "🧾 Ugry barlaň:\n\n"
            "🛫 Nireden: {origin}\n"
            "🛬 Nirä: {destination}\n"
            "📅 Sene: {date}\n\n"
            "Dogrumy?"
        ),
    },

    "searching": {
        "ru": "🔍 Ищу билеты, подождите немного...",
        "tk": "🔍 Bilet gözleýär, birazajyk garaşyň...",
    },
    "search_results_header": {
        "ru": "Вот что удалось найти по вашему запросу:",
        "tk": "Ine gözlegiňiz boýunça tapylanlar:",
    },
    "no_results": {
        "ru": (
            "😔 По этому маршруту и дате пока нет цен в базе.\n\n"
            "Это не значит, что рейсов нет — просто пока никто не искал именно "
            "эти даты. Можно:\n"
            "• Подписаться и мы пришлём уведомление, как только появится цена\n"
            "• Попробовать другую дату"
        ),
        "tk": (
            "😔 Bu ugur we sene boýunça bazada baha tapylmady heniz.\n\n"
            "Bu uçuş ýok diýmek däl — ýöne şu senäni entek hiç kim gözlemedi. "
            "Şulary edip bilersiňiz:\n"
            "• Yzarlama goýuň, baha peýda bolanda habar bereris\n"
            "• Başga sene synanyşyň"
        ),
    },
    "btn_subscribe": {"ru": "🔔 Подписаться на этот маршрут", "tk": "🔔 Bu ugry yzarla"},
    "btn_buy": {"ru": "🎫 Купить билет", "tk": "🎫 Bilet satyn al"},
    "btn_new_search": {"ru": "🔁 Новый поиск", "tk": "🔁 Täze gözleg"},

    "flight_card": {
        "ru": (
            "✈️ {origin} → {destination}\n"
            "📅 Дата вылета: {date}\n"
            "🔄 Пересадок: {transfers}\n"
            "💰 Цена: от {price} {currency}\n"
        ),
        "tk": (
            "✈️ {origin} → {destination}\n"
            "📅 Uçuş senesi: {date}\n"
            "🔄 Geçişler: {transfers}\n"
            "💰 Baha: {price} {currency} başlap\n"
        ),
    },
    "transfers_direct": {"ru": "прямой рейс", "tk": "göni uçuş"},
    "transfers_n": {"ru": "{n}", "tk": "{n}"},

    "subscribed_ok": {
        "ru": (
            "✅ Подписка создана!\n\n"
            "{origin} → {destination}\n"
            "Мы уведомим вас, как только увидим цену на этот маршрут "
            "или когда цена снизится."
        ),
        "tk": (
            "✅ Yzarlama döredildi!\n\n"
            "{origin} → {destination}\n"
            "Bu ugur boýunça baha peýda bolanda ýa-da baha arzanlanda "
            "size habar bereris."
        ),
    },

    "subs_empty": {
        "ru": (
            "У вас пока нет активных подписок.\n\n"
            "Найдите билеты и нажмите «Подписаться на этот маршрут», "
            "если цена вас не устроит — мы будем следить за ней вместо вас."
        ),
        "tk": (
            "Häzirlikçe hiç hili işjeň yzarlamaňyz ýok.\n\n"
            "Bilet gözläň we baha gowy görünmese \"Bu ugry yzarla\" düwmesine "
            "basyň — bahany siziň deregiňizde yzarlarys."
        ),
    },
    "subs_header": {
        "ru": "🔔 Ваши подписки:",
        "tk": "🔔 Sizin yzarlamalaryňyz:",
    },
    "sub_item": {
        "ru": "{i}. {origin} → {destination} · последняя известная цена: {price}",
        "tk": "{i}. {origin} → {destination} · soňky belli baha: {price}",
    },
    "sub_no_price_yet": {"ru": "пока нет данных", "tk": "heniz maglumat ýok"},
    "btn_delete_sub": {"ru": "🗑 Удалить", "tk": "🗑 Poz"},
    "sub_deleted": {"ru": "Подписка удалена ✅", "tk": "Yzarlama pozuldy ✅"},

    "price_drop_alert": {
        "ru": (
            "🔔 Новая цена по вашей подписке!\n\n"
            "✈️ {origin} → {destination}\n"
            "📅 {date}\n"
            "💰 {price} {currency}\n"
        ),
        "tk": (
            "🔔 Yzarlamaňyz boýunça täze baha!\n\n"
            "✈️ {origin} → {destination}\n"
            "📅 {date}\n"
            "💰 {price} {currency}\n"
        ),
    },

    "settings_menu": {
        "ru": "⚙️ Настройки. Текущий язык: Русский",
        "tk": "⚙️ Sazlamalar. Häzirki dil: Türkmen",
    },
    "btn_lang_ru": {"ru": "🇷🇺 Русский", "tk": "🇷🇺 Русский"},
    "btn_lang_tk": {"ru": "🇹🇲 Türkmençe", "tk": "🇹🇲 Türkmençe"},

    "same_city_error": {
        "ru": "⚠️ Города отправления и назначения не могут совпадать. Выберите другой город.",
        "tk": "⚠️ Uçuş we baryş şäherleri gabat gelip bilmez. Başga şäher saýlaň.",
    },
    "generic_error": {
        "ru": "⚠️ Что-то пошло не так. Попробуйте ещё раз чуть позже.",
        "tk": "⚠️ Bir zat nädogry boldy. Birazdan ýene synanyşyň.",
    },
    "action_cancelled": {
        "ru": "Действие отменено.",
        "tk": "Hereket ýatyryldy.",
    },
}


def t(key: str, lang: str, **kwargs) -> str:
    lang = lang if lang in ("ru", "tk") else "ru"
    template = TEXTS.get(key, {}).get(lang, key)
    if kwargs:
        return template.format(**kwargs)
    return template

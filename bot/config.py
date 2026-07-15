import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    bot_token: str
    tp_token: str
    tp_marker: str

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password: str

    sub_check_interval_minutes: int


def load_config() -> Config:
    return Config(
        bot_token=_require("BOT_TOKEN"),
        tp_token=_require("TP_TOKEN"),
        tp_marker=_require("TP_MARKER"),
        db_host=os.getenv("DB_HOST", "localhost"),
        db_port=int(os.getenv("DB_PORT", "5432")),
        db_name=os.getenv("DB_NAME", "tkm_bot"),
        db_user=os.getenv("DB_USER", "tkm_bot"),
        db_password=_require("DB_PASSWORD"),
        sub_check_interval_minutes=int(
            os.getenv("SUBSCRIPTION_CHECK_INTERVAL_MINUTES", "180")
        ),
    )


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise RuntimeError(
            f"Переменная окружения {key} не задана. Проверьте файл .env"
        )
    return value

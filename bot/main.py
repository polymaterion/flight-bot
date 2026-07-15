import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.config import load_config
from bot.db import database as db
from bot.handlers import search as search_handlers
from bot.handlers import settings, start, subscriptions
from bot.services.subscription_checker import check_all_subscriptions
from bot.services.travelpayouts import TravelpayoutsClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


async def main() -> None:
    config = load_config()

    await db.init_pool(
        host=config.db_host,
        port=config.db_port,
        name=config.db_name,
        user=config.db_user,
        password=config.db_password,
    )
    logger.info("Пул соединений с PostgreSQL инициализирован")

    tp_client = TravelpayoutsClient(token=config.tp_token, marker=config.tp_marker)
    # Прокидываем клиент в модуль search без глобального DI-фреймворка
    search_handlers.tp_client = tp_client

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(settings.router)
    dp.include_router(search_handlers.router)
    dp.include_router(subscriptions.router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_all_subscriptions,
        "interval",
        minutes=config.sub_check_interval_minutes,
        args=[bot, tp_client],
        id="subscription_price_check",
        next_run_time=None,  # первый прогон - по расписанию, не сразу при старте
    )
    scheduler.start()
    logger.info(
        "Планировщик подписок запущен, интервал: %d мин",
        config.sub_check_interval_minutes,
    )

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Бот запущен, начинаю polling")
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)
        await db.close_pool()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

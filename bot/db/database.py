"""
Слой работы с PostgreSQL через asyncpg.

Таблицы:
- users(user_id, lang, created_at)
- subscriptions(id, user_id, origin, destination, depart_date, last_price,
                last_currency, created_at)
"""

from datetime import date, datetime
from typing import Optional

import asyncpg

_pool: Optional[asyncpg.Pool] = None


async def init_pool(host: str, port: int, name: str, user: str, password: str) -> None:
    global _pool
    _pool = await asyncpg.create_pool(
        host=host, port=port, database=name, user=user, password=password,
        min_size=1, max_size=10,
    )
    await _create_tables()


async def close_pool() -> None:
    if _pool is not None:
        await _pool.close()


def pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Пул соединений с БД не инициализирован. Вызовите init_pool().")
    return _pool


async def _create_tables() -> None:
    async with pool().acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id BIGINT PRIMARY KEY,
                lang VARCHAR(2) NOT NULL DEFAULT 'ru',
                created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS subscriptions (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
                origin VARCHAR(3) NOT NULL,
                destination VARCHAR(3) NOT NULL,
                depart_date DATE,
                last_price NUMERIC,
                last_currency VARCHAR(3) DEFAULT 'RUB',
                created_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
            """
        )
        await conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_subscriptions_user
            ON subscriptions(user_id);
            """
        )


# ---------- users ----------

async def upsert_user(user_id: int, lang: str = "ru") -> None:
    async with pool().acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (user_id, lang) VALUES ($1, $2)
            ON CONFLICT (user_id) DO NOTHING;
            """,
            user_id, lang,
        )


async def set_user_lang(user_id: int, lang: str) -> None:
    async with pool().acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (user_id, lang) VALUES ($1, $2)
            ON CONFLICT (user_id) DO UPDATE SET lang = EXCLUDED.lang;
            """,
            user_id, lang,
        )


async def get_user_lang(user_id: int) -> str:
    async with pool().acquire() as conn:
        row = await conn.fetchrow(
            "SELECT lang FROM users WHERE user_id = $1;", user_id
        )
        return row["lang"] if row else "ru"


# ---------- subscriptions ----------

async def add_subscription(
    user_id: int,
    origin: str,
    destination: str,
    depart_date: Optional[date],
    last_price: Optional[float] = None,
    last_currency: str = "RUB",
) -> int:
    async with pool().acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO subscriptions
                (user_id, origin, destination, depart_date, last_price, last_currency)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id;
            """,
            user_id, origin, destination, depart_date, last_price, last_currency,
        )
        return row["id"]


async def get_user_subscriptions(user_id: int) -> list[asyncpg.Record]:
    async with pool().acquire() as conn:
        return await conn.fetch(
            """
            SELECT id, origin, destination, depart_date, last_price, last_currency
            FROM subscriptions
            WHERE user_id = $1
            ORDER BY created_at DESC;
            """,
            user_id,
        )


async def delete_subscription(sub_id: int, user_id: int) -> None:
    async with pool().acquire() as conn:
        await conn.execute(
            "DELETE FROM subscriptions WHERE id = $1 AND user_id = $2;",
            sub_id, user_id,
        )


async def get_all_subscriptions() -> list[asyncpg.Record]:
    """Для планировщика: все подписки всех пользователей."""
    async with pool().acquire() as conn:
        return await conn.fetch(
            """
            SELECT s.id, s.user_id, s.origin, s.destination, s.depart_date,
                   s.last_price, s.last_currency, u.lang
            FROM subscriptions s
            JOIN users u ON u.user_id = s.user_id;
            """
        )


async def update_subscription_price(sub_id: int, price: float, currency: str) -> None:
    async with pool().acquire() as conn:
        await conn.execute(
            """
            UPDATE subscriptions
            SET last_price = $1, last_currency = $2
            WHERE id = $3;
            """,
            price, currency, sub_id,
        )

import aiohttp

from src.config import settings
from src.exceptions import BinAPIError
from src.init import redis_manager


def normalize_bin(raw_bin: str) -> str:  # покрыть тестом
    digits = "".join(c for c in raw_bin if c.isascii() and c.isdigit())
    if len(digits) < 6 or len(digits) > 8:
        raise BinAPIError

    return digits[:6]

async def get_bin_cards(bin_cards: str, user_id: int | None = None) -> str:
    clean_bin = normalize_bin(bin_cards)
    cache_key = f"bin:{clean_bin}"

    bin_from_cache = await redis_manager.get(cache_key)
    if bin_from_cache:
        return bin_from_cache

    if user_id and redis_manager.redis:
        throttle_key = f"throttle:user:{user_id}"
        is_allowed = await redis_manager.redis.set(throttle_key, "1", ex=3, nx=True)
        if not is_allowed:
            raise BinAPIError


    my_headers = {"x-api-key": settings.KEY_BIN}
    url = f"https://data.handyapi.com/bin/{clean_bin}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=my_headers) as response:
            data = await response.json()
            if response.status == 200 and data.get("Status") == "SUCCESS":
                issuer = data.get("Issuer") or "Неизвестный банк"
                payment_system = data.get("Scheme") or "Не определена"
                card_type = data.get("Type") or "Не определён"
                country = (data.get("Country") or {}).get("Name") or "Не определена"

                result = (
                    f"🏦 Банк: {issuer}\n"
                    f"💳 Система: {payment_system}\n"
                    f"📄 Тип: {card_type}\n"
                    f"🌍 Страна: {country}"
                )
                await redis_manager.set(cache_key, result, expire=86400)

                return result
            print(f"Ошибка API. Ответ сервера: {data}")
            raise BinAPIError
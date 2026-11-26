import aiohttp
import re

from src.config import settings
from src.exceptions import PhoneAPIError
from src.init import redis_manager


def normalize_phone(raw_phone: str) -> str: # покрыть тестом
    digits = re.sub(r"\D", "", raw_phone)
    if len(digits) < 9 or len(digits) > 15:
        raise PhoneAPIError

    # Если это 11-значный российский номер на 7 или 8 — убираем первую цифру
    if len(digits) == 11 and digits[0] in ("7", "8"):
        return digits[1:]

    return digits


async def get_region_by_phone(phone: str, user_id: int | None = None) -> str:
    clean_phone = normalize_phone(phone)
    cache_key = f"phone:{clean_phone}"

    phone_from_cache = await redis_manager.get(cache_key)
    if phone_from_cache:
        return phone_from_cache

    if user_id and redis_manager.redis:
        throttle_key = f"throttle:user:{user_id}"
        is_allowed = await redis_manager.redis.set(throttle_key, "1", ex=3, nx=True)
        if not is_allowed:
            raise PhoneAPIError

    key = settings.KEY_PHON
    my_headers = {"X-API-Key": key}
    url = f"https://num7.ru/v1/lookup?phone={clean_phone}"

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url, headers=my_headers) as response:
                if response.status == 200:
                    data = await response.json()

                    operator = data.get("operator") or "Оператор не определён"
                    region = data.get("region") or "Регион не определён"

                    result = f"{operator}, {region}"
                    await redis_manager.set(cache_key, result, expire=86400)
                    return result

                print(f"Ошибка num7.ru [{response.status}]: {await response.text()}")
                raise PhoneAPIError

    except (aiohttp.ClientError, TimeoutError) as e:
        print(f"Сетевая ошибка при запросе к num7.ru: {e}")
        raise PhoneAPIError from e




async def get_balance() -> dict:
    key = settings.KEY_PHON
    my_headers = {"X-API-Key": key}
    url = "https://num7.ru/v1/balance"

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(url, headers=my_headers) as response:
                if response.status == 200:
                    return await response.json()

                print(f"Ошибка num7.ru при проверке баланса [{response.status}]: {await response.text()}")
                raise PhoneAPIError

    except (aiohttp.ClientError, TimeoutError) as e:
        print(f"Сетевая ошибка при проверке баланса num7.ru: {e}")
        raise PhoneAPIError from e
import aiohttp
from src.config import settings
from src.exceptions import PhoneAPIError


async def get_region_by_phone(phone: str) -> str:
    key = settings.KEY_PHON
    my_headers = {"X-API-Key": key}
    url = f'https://num7.ru/v1/lookup?phone={phone}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=my_headers) as response:
                if response.status == 200:
                    data = await response.json()
                    operator = data.get("operator") or "Оператор не определён"
                    region = data.get("region") or "Регион не определён"
                    return f"{operator}, {region}"
                print(await response.json())
                print(f"Ошибка num7.ru [{response.status}]: {await response.text()}")
                raise PhoneAPIError

    except aiohttp.ClientError as e:
        print(f"Сетевая ошибка при запросе к num7.ru: {e}")
        raise PhoneAPIError from e
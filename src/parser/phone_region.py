import aiohttp
from src.config import settings
from src.exceptions import PhoneAPIError


async def get_region_by_phone(phone: str) -> str:
    key = settings.KEY_PHON
    my_headers = {"X-API-Key": key}
    url = f'https://num7.ru/v1/lookup?phone={phone}'


    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=my_headers) as response:
            if response.status == 200:
                data = await response.json()
                return f'{data.get("operator")}, {data.get("region")}'
            print(await response.json())
            raise PhoneAPIError
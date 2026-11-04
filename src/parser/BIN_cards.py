import aiohttp
from src.exceptions import BinAPIError


async def get_bin_cards(bin_cards: str) -> str:
    my_headers = {"x-api-key": "HAS-140cYW2Q84HBWT5gk7jPZXU"}
    url = f'https://data.handyapi.com/bin/{bin_cards}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=my_headers) as response:
            data = await response.json()
            if response.status == 200:
                issuer_info = data.get('Issuer', 'Неизвестный банк')
                return f"{issuer_info}"
            print(f"Ошибка API. Ответ сервера: {data}")
            raise BinAPIError



















try:
    response = requests.get(
        "https://data.handyapi.com/bin/535316",
        headers={"x-api-key": "your key"}
    )
    data = response.json()
    print(data)  # debug
except Exception as e:
    print("Request failed:", e)
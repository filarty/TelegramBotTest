import aiohttp
import asyncio


class Account:
    def __init__(self, token: str) -> None:
        self.TOKEN = token  # KEY FROM TINKOFF see: https://tinkoffcreditsystems.github.io/invest-openapi/

    async def response(self):
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {self.TOKEN}'}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api-invest.tinkoff.ru/openapi/portfolio', headers=headers) as response:
                return await response.json()

    async def get_porfolio(self):
        response = await self.response()
        return [f"{i['name']} : {i['balance']}" for i in response['payload']['positions']]


if __name__ == "__main__":
    account = Account("")
    print(account.get_porfolio())

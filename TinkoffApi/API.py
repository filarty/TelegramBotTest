import aiohttp
import asyncio


class Account:
    def __init__(self, token: str) -> None:
        self.TOKEN = token
        self.portfolio = None

    async def response(self):
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {self.TOKEN}'}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api-invest.tinkoff.ru/openapi/portfolio', headers=headers) as response:
                portfolio = await response.json()
                self.portfolio = [f"{i['name']} : {i['balance']}" for i in portfolio['payload']['positions']]


if __name__ == "__main__":
    account = Account("")

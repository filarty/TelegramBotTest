import aiohttp
import asyncio


class Account:
    def __init__(self, token: str) -> None:
        self.TOKEN = token  # KEY FROM TINKOFF see: https://tinkoffcreditsystems.github.io/invest-openapi/
        self.loop = asyncio.get_event_loop()

    async def response(self):
        headers = {'accept': 'application/json', 'Authorization': f'Bearer {self.TOKEN}'}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api-invest.tinkoff.ru/openapi/portfolio', headers=headers) as response:
                return await response.json()

    def get_porfolio(self):
        response = self.loop.run_until_complete(self.response())
        return [f"{i['name']} : {i['balance']}" for i in response['payload']['positions']]


if __name__ == "__main__":
    account = Account("")
    print(account.get_porfolio())

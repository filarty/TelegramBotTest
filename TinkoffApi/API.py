import aiohttp


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
        return [f"+++ {i['name']} +++ \nКоличество бумаг: {int(i['balance'])}\n" \
                f"Цена за штуку: {int(i['averagePositionPrice']['value'] * 100) / 100}\n" \
                f"Общая сумма: {int(i['averagePositionPrice']['value'] * i['balance'] + i['expectedYield']['value'])}"
                for i in response['payload']['positions']]


if __name__ == "__main__":
    account = Account("")
    print(account.get_porfolio())

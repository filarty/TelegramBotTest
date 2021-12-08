import logging

import asyncio

from aiogram import Bot, Dispatcher, executor, types

import DataBaseBot

from Keyboard import keyboard

from TinkoffApi import API

from settings import BOT_TOKEN




logging.basicConfig(level=logging.INFO)
TOKEN = BOT_TOKEN


class TelegramBot:
    def __init__(self, token: str) -> None:
        self.loop = asyncio.get_event_loop()
        self.bot = Bot(token)
        self.dp = Dispatcher(self.bot)

    def messages(self):
        @self.dp.message_handler(commands=['start', 'help'])
        async def send(message: types.Message):
            self.add_to_database(message.from_user.id, message.from_user.username)
            await self.bot.send_message(message.from_user.id, reply_markup=keyboard,
                                        text="Привет {}".format(message.from_user.username))

        @self.dp.message_handler()
        async def get_message(message: types.Message):
            if message.text == '💼 Ваш портфель в тинькофф':
                result = await self.get_portfolio()
                result = '\n'.join(result)
                await self.bot.send_message(message.from_user.id, result)

    async def get_portfolio(self):
        account = API.Account("")
        await account.response()
        return account.portfolio

    def add_to_database(self, user_id: str, username: str):
        user = DataBaseBot.User(user_id=int(user_id), user_name=username)
        try:
            DataBaseBot.session.add(user)
            DataBaseBot.session.commit()
        except:
            return

    def start(self):
        self.messages()
        executor.start_polling(self.dp, skip_updates=True)


TeleBot = TelegramBot(TOKEN)

if __name__ == "__main__":
    TeleBot.start()

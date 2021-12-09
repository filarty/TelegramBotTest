import logging

from aiogram import Bot, Dispatcher, executor, types

import aiohttp

import DataBaseBot

from Keyboard import keyboard

from TinkoffApi import API

from settings import BOT_TOKEN

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

logging.basicConfig(level=logging.INFO)
TOKEN = BOT_TOKEN
storage = MemoryStorage()


class Form(StatesGroup):
    api = State()


class TelegramBot:
    def __init__(self, token: str) -> None:
        self.bot = Bot(token)
        self.dp = Dispatcher(self.bot, storage=storage)

    def messages(self):
        @self.dp.message_handler(commands=['start', 'help'])
        async def send(message: types.Message):
            self.add_to_database(message.from_user.id, message.from_user.username)
            await self.bot.send_message(message.from_user.id, reply_markup=keyboard,
                                        text="Привет {}".format(message.from_user.username))

        @self.dp.message_handler()
        async def get_message(message: types.Message):
            if message.text == '💼 Ваш портфель в тинькофф':
                try:
                    result = await self.get_portfolio(message.from_user.id)
                    result = '\n'.join(result)
                    await message.reply(result)
                except aiohttp.ContentTypeError:
                    await message.reply("Неверный ключ API!")

            elif message.text == '🏦 Установить API ключ':
                await Form.api.set()
                await self.bot.send_message(message.from_user.id, "Напишите ваш ключ")

        @self.dp.message_handler(state=Form.api)
        async def set_API(message: types.Message, state: FSMContext):
            user = DataBaseBot.session.query(DataBaseBot.User).where(
                DataBaseBot.User.user_id == message.from_user.id).one()
            async with state.proxy() as data:
                data['api'] = message.text
                user.API_key = data['api']
            DataBaseBot.session.commit()
            await message.reply("API ключ успешно установлен!")
            await state.finish()

    def add_to_database(self, user_id: str, username: str):
        user = DataBaseBot.User(user_id=int(user_id), user_name=username)
        try:
            DataBaseBot.session.add(user)
            DataBaseBot.session.commit()
        except:
            return

    async def get_portfolio(self, user_id):
        user = DataBaseBot.session.query(DataBaseBot.User).where(
            DataBaseBot.User.user_id == user_id).one()
        account = API.Account(user.API_key)
        result = await account.get_porfolio()
        return result

    def start(self):
        self.messages()
        executor.start_polling(self.dp, skip_updates=True)


TeleBot = TelegramBot(TOKEN)

if __name__ == "__main__":
    TeleBot.start()

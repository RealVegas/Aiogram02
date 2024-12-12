import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from googletrans import Translator

from config_data.bot_config import BOT_TOKEN

bot: Bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

translator: Translator = Translator()


async def set_commands(robot: Bot) -> None:
    commands = [
        types.BotCommand(command='/start', description='Запустить бота'),
        types.BotCommand(command='/help', description='Помощь'),
        types.BotCommand(command='/weather', description='Погода в Екатеринбурге'),
    ]
    await robot.set_my_commands(commands)


@dp.message(Command('help'))
async def bot_help(message: Message):
    # trans_text: str = translator.translate(quote_text, dest='ru').text
    await message.answer(
        'Этот бот умеет выполнять команды:\n/start - приветствие\n/help - помощь\n/weather - погода в Екатеринбурге')


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я бот!')


async def main():
    await set_commands(bot)
    print('Бот запущен')
    await dp.start_polling(bot)


async def stop_bot() -> None:
    await bot.session.close()
    print('Бот остановлен')


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        asyncio.run(stop_bot())
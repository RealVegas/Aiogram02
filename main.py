import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, Message
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


async def clear_commands(robot: Bot) -> None:
    await robot.set_my_commands([])
    await clear_commands(bot)


@dp.message(F.photo)
async def save_photo(message: Message):
    await bot.download(message.photo[-1], destination=f'images/{message.photo[-1].file_id}.jpg')
    await message.answer('Картинка сохранена')


@dp.message(Command('voice'))
async def bot_voice(message: Message):
    voice = FSInputFile('audio/voice.ogg')
    await message.answer_voice(voice)


@dp.message(CommandStart())
async def bot_start(message: Message):
    await message.answer('Привет! Я бот-переводчик, еще я умею сохранять картинки и отправлять голосовое сообщение')


@dp.message(Command('help'))
async def bot_help(message: Message):
    await message.answer(
        'Этот бот умеет выполнять команды:\n'
        '/start - приветствие и возможности\n'
        '/help - помощь\n'
        '/voice - отправляет голосовое сообщение\n'
        'Когда вы отправляет боту текстовое сообщение, он переводит его на английский язык\n'
        'Если вы отправите ему изображение, бот сохранит его в папку /images')


@dp.message()
async def trans(message: Message):
    trans_message: str = translator.translate(message.text, dest='en').text
    await message.answer('Перевод: ' + trans_message)


async def main():
    # await set_commands(bot)
    # await clear_commands(bot)
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
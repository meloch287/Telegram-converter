import asyncio
from aiogram import Bot, Dispatcher, F
from handlers import router

async def main():
    bot = Bot(token='7525690138:AAFdojSGaRqL3idPaO_7hJsd_NpcH9aeic8')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('ЗАПУСК ШАЙТАН МАШИНЫ')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')
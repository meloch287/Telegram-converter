import asyncio
from aiogram import Bot, Dispatcher, F
from handlers import router

async def main():
    bot = Bot(token='-Заглушка-')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('ЗАПУСК ШАЙТАН МАШИНЫ')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('EXIT')

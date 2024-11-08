import asyncio
from dotenv import load_dotenv
import os
import threading
from handlers import router, check_price
from aiogram import Bot, Dispatcher

def wrap_check_price():
    asyncio.run(check_price())

async def main():
    threading.Thread(target=wrap_check_price).start()
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Exit')
import asyncio
from dotenv import load_dotenv
import os
from handlers import router, check_price
from aiogram import Bot, Dispatcher

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    asyncio.create_task(check_price(bot))
    await dp.start_polling(bot)


if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Exit')
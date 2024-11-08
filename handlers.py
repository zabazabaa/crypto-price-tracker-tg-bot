import os
from dotenv import load_dotenv

import checkPrice as cp
import asyncio

from aiogram import Bot, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='add task📄')],
    [KeyboardButton(text='delete task🗑')]
    ],
                                     resize_keyboard=True)

crypto_ids = ['bitcoin', 'etherium', 'solana']

router = Router()
load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))

async def check_price():
    await asyncio.sleep(1)
    while True:
        await asyncio.sleep(20)
        for i in cp.read_task_file():
            print(i)
            coin = i
            alertPrice = cp.read_task_file()[i]
            price = await cp.get_price(coin)
            try:
                if price >= alertPrice:
                    await bot.send_message(chat_id=os.getenv('CHAT_ID') ,text=f'{i} price is {price} usd')
                    cp.delete_task_in_file(coin)
            except:
                pass

class add_tasks(StatesGroup):
    coin_name = State()
    alertPrice = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Welcome to crypto price tracker bot', reply_markup=start_keyboard)

@router.message(F.text == 'add task📄')
async def add_task(message: Message, state: FSMContext):
    await message.answer('Enter coin name')
    await state.set_state(add_tasks.coin_name)

@router.message(add_tasks.coin_name)
async def add_task(message: Message, state: FSMContext):
    await state.update_data(coin_name=message.text)
    await message.answer('Enter alert price')
    await state.set_state(add_tasks.alertPrice)

@router.message(add_tasks.alertPrice)
async def add_task(message: Message, state: FSMContext):
    await state.update_data(alertPrice=message.text)
    data = await state.get_data()
    #valid test
    if data['coin_name'] in crypto_ids:
        try:
            data['alertPrice'] = float(data['alertPrice'])
            cp.add_task_to_file(data)
            await message.answer('task added✅')
        except:
            await message.answer('invalid alert price❌')
    else:
        await message.answer('cannot find this crypto❌')
    await state.clear()

@router.message(F.text == 'delete task🗑')
async def delete_task(message: Message, state: FSMContext):
    await message.answer('Enter coin name')
    await state.set_state(add_tasks.coin_name)

@router.message(add_tasks.coin_name)
async def delete_task(message: Message, state: FSMContext):
    await state.update_data(coin_name=message.text)
    data = await state.get_data()
    if data['coin_name'] in crypto_ids:
        cp.delete_task_in_file(data['coin_name'])    
        await message.answer('task deleted✅')
    else:
        await message.answer('cannot find this task')
    await state.clear()
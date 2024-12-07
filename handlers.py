import os

import checkPrice as cp
import asyncio

from aiogram import Bot, Router, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

start_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='add/edit task📄')],
    [KeyboardButton(text='delete task🗑')]
    ],
                                     resize_keyboard=True)

async def delete_task_kb(coin_name):
    builder = InlineKeyboardBuilder()
    builder.button(text='delete', callback_data=f'delete_{coin_name}')
    return builder.as_markup()

crypto_ids = ['bitcoin', 'etherium', 'solana']

router = Router()

async def check_price(bot: Bot):
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
            except Exception as e:
                print(e)

class add_tasks(StatesGroup):
    coin_name = State()
    alertPrice = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Welcome to crypto price tracker bot', reply_markup=start_keyboard)

@router.message(F.text == 'add/edit task📄')
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
    tasks = cp.read_task_file()
    if tasks:
        await message.answer('Your tasks:')
        for coin in tasks:
            await message.answer(f'{coin}\nalert price: {tasks[coin]}', reply_markup=await delete_task_kb(coin))
    else:
        await message.answer('You have no tasks❌')

@router.callback_query(F.data.startswith('delete_'))
async def delete_task(callback: CallbackQuery):
    coin_name = callback.data.split('_')[1]
    cp.delete_task_in_file(coin_name)
    await callback.message.edit_text('task deleted✅')
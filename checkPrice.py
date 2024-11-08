import json
import aiohttp

COINGECKO_API_URL = 'https://api.coingecko.com/api/v3'
currency='usd'

async def get_price(crypto_id):
    url = f'{COINGECKO_API_URL}/simple/price'
    params = {
        'ids': crypto_id,
        'vs_currencies': currency
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return (await response.json())[crypto_id][currency]

def read_task_file():
    with open('tasks.json', encoding='utf-8') as file:
        return json.load(file)

def add_task_to_file(data):
    tasks = read_task_file()
    tasks[data['coin_name']] = float(data['alertPrice'])
    with open('tasks.json', 'w', encoding='utf-8') as file:
        json.dump(tasks, file, indent=4)

def delete_task_in_file(coin_name):
    tasks = read_task_file()
    try:
        del tasks[coin_name]
        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(tasks, file, indent=4)
    except KeyError as e:
        print(f'Error {e}')

if __name__ == '__main__':
    #add_task_to_file({'name': 'abc', 'alertPrice': 1234})
    #delete_task_in_file('a')
    print(get_price('bitcoin'))
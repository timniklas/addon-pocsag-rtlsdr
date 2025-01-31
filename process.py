import sys
import re
import os
import aiohttp
import asyncio
from enum import Enum
from time import gmtime, strftime
import json

pattern = r"POCSAG1200:\s+Address:\s+(\d+)\s+Function:\s+(\d)"
VALUES=['a','b','c','d']

SUPERVISOR_TOKEN=os.environ['SUPERVISOR_TOKEN']

def loadConfig():
        with open('/data/options.json') as config_file:
                return json.load(config_file)

async def fire_event(event_type: str, payload):
        async with aiohttp.ClientSession() as websession:
                async with websession.post(f'http://supervisor/core/api/events/{event_type}',
                headers={
                        'Authorization': f'Bearer {SUPERVISOR_TOKEN}'
                },
                json=payload) as response:
                        response.raise_for_status()

def listStartswith(items: list, key: str):
        for item in items:
                if key.startswith(item):
                        return True
        return False

CONFIG=loadConfig()
CONFIG_IGNORE_ADDRESSES=CONFIG['ignore_addresses']
if len(CONFIG_IGNORE_ADDRESSES) > 0:
        print('Ignoring the following addresses: ')
        for address in CONFIG_IGNORE_ADDRESSES:
                print(address)

for line in sys.stdin:
        if 'Exit' == line.rstrip():
                break
        if "No supported devices found." in line:
                break
        result = re.search(pattern, line)
        if result:
                pocsag_address = result[1].rjust(7, '0')
                key = result[2]
                pocsag_function = VALUES[int(key)]
                local_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                full_address = pocsag_address + pocsag_function
                if not listStartswith(CONFIG_IGNORE_ADDRESSES, full_address):
                        print(f"{local_time}: PROCESSING {pocsag_address} {pocsag_function}")
                        asyncio.run(fire_event('pocsag_receive', {
                                'address': pocsag_address,
                                'function': pocsag_function
                        }))
                else:
                        print(f"{local_time}: IGNORING {pocsag_address} {pocsag_function}")

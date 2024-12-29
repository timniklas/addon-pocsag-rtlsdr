import sys
import re
import os
import aiohttp
import asyncio
from enum import Enum
from time import gmtime, strftime

pattern = r"POCSAG1200:\s+Address:\s+(\d+)\s+Function:\s+(\d)"
VALUES=['a','b','c','d']

SUPERVISOR_TOKEN=os.environ['SUPERVISOR_TOKEN']

async def fire_event(event_type: str, payload):
        async with aiohttp.ClientSession() as websession:
                async with websession.post(f'http://supervisor/core/api/events/{event_type}',
                headers={
                        'Authorization': f'Bearer {SUPERVISOR_TOKEN}'
                },
                json=payload) as response:
                        response.raise_for_status()

async def publish(pocsag_address: str, pocsag_function: str):
        try:
                await fire_event('pocsag_receive', {
                        'address': pocsag_address,
                        'function': pocsag_function
                })
        except Exception as e:
                print(e)

for line in sys.stdin:
        if 'Exit' == line.rstrip():
                break
        if "No supported devices found." in line:
                break
        result = re.search(pattern, line)
        if result:
                addr = result[1].rjust(7, '0')
                key = result[2]
                func = VALUES[int(key)]
                local_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                
                print(f"{local_time}: RIC {addr} {func}")
                asyncio.run(publish(addr, func))

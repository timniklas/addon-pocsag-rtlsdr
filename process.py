import sys
import re
import asyncio
from enum import Enum
from time import gmtime, strftime

pattern = r"POCSAG1200:\s+Address:\s+(\d+)\s+Function:\s+(\d)"
VALUES=['a','b','c','d']

async def publish(addr: str, func: str):
        try:
          #push to ha
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

import os
import sys
import time
import aiohttp
import asyncio
import aiofiles


async def get_photo(session, folder: str, image_name: str):
    url = "https://picsum.photos/200"

    response = await session.get(url)
    content = await response.read()
    f = await aiofiles.open(os.path.join(folder, image_name), mode='wb')
    await f.write(content)
    await f.close()


async def main(num_of_photos: int = 10, folder: str = "test"):
    if not os.path.exists(folder):
        os.mkdir(folder)

    async with aiohttp.ClientSession(trust_env=True) as session:  
        await asyncio.gather(*((get_photo(session, folder, f"image{i}.jpeg")) for i in range(num_of_photos))) 


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(num_of_photos=int(sys.argv[1]), folder=sys.argv[2]))
    finally:
        loop.close()

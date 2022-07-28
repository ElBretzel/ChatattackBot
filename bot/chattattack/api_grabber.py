import os
import io

import aiohttp

# ###############################################################
#                        CATAPI.COM STUFF                      #
# ###############################################################

async def cat_request(url, key = None, path = "json"):
    # Request specified URL and return Response object
    headers = {"x-api-key": key}
    async with aiohttp.ClientSession(headers = headers) as session:
        async with session.get(url) as resp:
            if path == "json":
                return await resp.json()
            elif path == "fp":
                return io.BytesIO(await resp.read())
            else:
                raise "[CATAPI] Wrong path"


# image = Image.open(fp=await cat_request(image, KEY, "fp").content)
# image.show()


# ###############################################
# #                 Stats (0 - 5)                #
# ################################################

# name = cat_data[0]["breeds"][0]["name"]


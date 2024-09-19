import asyncio

from main import main, settings

asyncio.run(main(), debug=settings.DEBUG)
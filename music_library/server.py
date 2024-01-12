from tornado import web
import asyncio

from app import Index, Delete, MusicUpdate


def make_app():
    return web.Application([
        (r'/', Index),
        (r'/delete-music/', Delete),
        (r'/music-update/', MusicUpdate)
    ])


async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
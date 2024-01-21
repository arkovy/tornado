from tornado import web, ioloop
import argparse
import asyncio

from app import Index, Delete, MusicUpdate


def make_app():
    return web.Application([
        (r'/', Index),
        (r'/delete-music/', Delete),
        (r'/music-update/', MusicUpdate)
    ])


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()

    app = make_app()

    try:
        app.listen(args.port)
        print(f'Ваш порт: {args.port}')
        await asyncio.Future()
    except ValueError:
        print('Увы, вы ввели число больше или меньше указанного, повторите попытку')


if __name__ == "__main__":
    asyncio.run(main())

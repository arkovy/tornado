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
    try:
        app_listen = int(input('Введите номер порта, состоящий из 4 цыфр: '))
        if len(str(app_listen)) == 4:
            app.listen(int(app_listen))
            print(f'Ваш порт: {app_listen}')
        else:
            print('Увы, вы ввели число больше или меньше указанного, повторите попытку')
    except ValueError:
        print('Вы ввели не число!')
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

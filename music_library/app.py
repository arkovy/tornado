from tornado import web, websocket, ioloop
from sqlalchemy.orm import sessionmaker


from db import engine
from models import Music


class Index(web.RequestHandler):

    def get(self):
        session = sessionmaker(bind=engine)()
        context = {
            'musics': session.query(Music).all()
        }
        self.render('templates/index.html', **context)

    def post(self):
        session = sessionmaker(bind=engine)()
        music = Music(
            name=self.get_body_argument('input-text')
        )
        session.add(music)
        session.commit()
        server = ioloop.IOLoop.current()
        server.add_callback(MusicUpdate.send_message, 'hhsbabjds')
        context = {
            'musics': session.query(Music).all()
        }
        self.render('templates/index.html', **context)


class Delete(web.RequestHandler):

    def post(self):
        session = sessionmaker(bind=engine)()
        music = session.query(Music).filter_by(
            id=self.get_body_argument('id')
        ).first()
        session.delete(music)
        session.commit()
        self.redirect('/')


class MusicUpdate(websocket.WebSocketHandler):
    clients = []

    def open(self, *args: str, **kwargs: str):
        MusicUpdate.clients.append(self)
        super(MusicUpdate, self).open(*args, **kwargs)

    def close(self, code=None, reason=None):
        MusicUpdate.clients.remove(self)

    @classmethod
    def send_message(cls, message):
       for client in cls.clients:
           client.write_message(message)

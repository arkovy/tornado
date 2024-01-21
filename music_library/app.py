from tornado import web, websocket, ioloop
from sqlalchemy.orm import sessionmaker

from db import engine
from models import Music


class Index(web.RequestHandler):
    session = None

    def initialize(self):
        if Index.session is None:
            Index.session = sessionmaker(bind=engine)()

    def get(self):
        context = {
            'musics': self.session.query(Music).all()
        }
        self.render('templates/index.html', **context)

    def post(self):
        music = Music(
            name=self.get_body_argument('input-text')
        )
        self.session.add(music)
        self.session.commit()
        server = ioloop.IOLoop.current()
        server.add_callback(MusicUpdate.send_message, 'hhsbabjds')
        context = {
            'musics': self.session.query(Music).all()
        }
        self.render('templates/index.html', **context)


class Delete(web.RequestHandler):

    def post(self):
        music = Index.session.query(Music).filter_by(
            id=self.get_body_argument('id')
        ).first()
        Index.session.delete(music)
        Index.session.commit()
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

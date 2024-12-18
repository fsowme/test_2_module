from .handler import app

bans = app.Table('bans', default=list)

from .handler import app

bans = app.GlobalTable('bans', default=list)

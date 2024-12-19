from .handler import app

bans = app.GlobalTable('bans', default=list)
obscene_words = app.GlobalTable('obscene_words', default=list)

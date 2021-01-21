from datetime import datetime

import params

from Gideon.database.database import Database
from Gideon.database.models import models, Newspaper


def clear(engine_url):
    db = Database(engine_url)
    for model in models:
        db.drop_table(model)
        db.create_table(model)


if __name__ == '__main__':
    clear(params.db_url)

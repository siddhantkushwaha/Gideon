import os
import json

project_dir = os.path.dirname(os.path.realpath(__file__))

db_url = f"sqlite:///{os.path.join(project_dir, 'Gideon/database/db.sqlite')}"

with open(os.path.join(project_dir, 'tokens.json'), 'r') as fp:
    token = json.load(fp)

bot_username = token['bot_username']
gideon_token = token['Gideon']

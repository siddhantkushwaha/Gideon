import os
import json

project_dir = os.path.dirname(os.path.realpath(__file__))

db_url = f"sqlite:///{os.path.join(project_dir, 'Gideon/database/db.sqlite')}"
gideon_token = json.loads(os.path.join(project_dir, 'tokens.json'))['Gideon']

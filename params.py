import os
import json

project_dir = os.path.dirname(os.path.realpath(__file__))

db_url = f"sqlite:///{os.path.join(project_dir, 'Gideon/database/db.sqlite')}"

todd_path = os.path.join(project_dir, 'Gideon/lib/todd.jar')
downloads_dir = os.path.join(project_dir, 'downloads')

with open(os.path.join(project_dir, 'config.json'), 'r') as fp:
    config = json.load(fp)

bot_username = config['bot_username']
gideon_token = config['Gideon']
newspaper_archive_drive_folder_id = config['newspaper_archive_drive_folder_id']
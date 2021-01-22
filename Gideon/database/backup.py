import os
import logging

from Gideon.common import set_log_level
from Gideon.storage.todd import upload
from params import project_dir, newspaper_archive_drive_folder_id


def backup():
    db_path = os.path.join(project_dir, 'db.sqlite')
    ret = upload(db_path, newspaper_archive_drive_folder_id, overwrite=True)
    if ret is not None:
        logging.info(f'DB backed up at {ret}')


if __name__ == '__main__':
    set_log_level(logging.DEBUG)
    backup()

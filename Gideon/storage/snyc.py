import os
import shutil
import logging

from Gideon.common import set_log_level
from Gideon.database.database import Database
from Gideon.database.models import Newspaper
from Gideon.storage.todd import download, upload
from params import project_dir, db_url, downloads_dir, newspaper_archive_drive_folder_id


def sync(clear_cache=True):
    # change current working directory (to pick jar tokens correctly)
    os.chdir(project_dir)

    db = Database(db_url)
    papers = db.session.query(Newspaper).filter_by(drive_file_id='NONE').all()
    for paper in papers:
        file_name = f"{paper.name}-{paper.edition}-{paper.language}-{paper.type}-{paper.timestamp.strftime('%d-%B-%Y')}"
        file_name = file_name.replace(' ', '_')
        logging.info(f'Downloading paper: {file_name}')

        if 'drive.google.com' in paper.link:
            file_id = list(filter(lambda x: len(x) == 33, paper.link.split('/')))[0]
            download_dir = os.path.join(downloads_dir, file_name)

            ret = download(file_id, download_dir)
            if not ret:
                raise Exception(f'Download failed for paper: {file_name}')

            pdf_path = list(filter(lambda x: x.endswith('.pdf'), os.listdir(download_dir)))[0]
            pdf_path = os.path.join(download_dir, pdf_path)

            new_pdf_path = os.path.join(download_dir, f'{file_name}.pdf')
            if os.path.exists(new_pdf_path):
                os.remove(new_pdf_path)

            shutil.copy(pdf_path, new_pdf_path)

            ret = upload(new_pdf_path, newspaper_archive_drive_folder_id)

            if ret is not None:
                logging.info(f'Paper uploaded at: {ret}')
                db.session.query(Newspaper).filter_by(id=paper.id).update({'drive_file_id': ret})
                db.session.commit()

                if clear_cache and os.path.exists(download_dir):
                    shutil.rmtree(download_dir)
            else:
                raise Exception(f'Failed to upload paper. {file_name}')

    db.session.close()


if __name__ == '__main__':
    set_log_level(logging.DEBUG)
    sync(clear_cache=True)

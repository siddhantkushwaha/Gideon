import logging
import subprocess

from params import todd_path


def download(file_id, download_dir):
    process = subprocess.Popen(
        ['java', '-jar', todd_path, 'download', file_id, download_dir, 'false'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout = process.stdout.read().decode()
    stderr = process.stderr.read().decode()

    if len(stdout) > 0:
        logging.info(stdout)

    if len(stderr) > 0:
        logging.error(stderr)

    return 'Download successful.' in stdout


def upload(file_path, parent_folder_id):
    process = subprocess.Popen(
        ['java', '-jar', todd_path, 'upload', file_path, parent_folder_id, 'false'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout = process.stdout.read().decode()
    stderr = process.stderr.read().decode()

    if len(stdout) > 0:
        logging.info(stdout)

    if len(stderr) > 0:
        logging.error(stderr)

    idx = stdout.find('Uploaded:')
    if idx > -1:
        file_id = stdout[idx + 10:].strip()
        return file_id if len(file_id) == 33 else None
    else:
        return None

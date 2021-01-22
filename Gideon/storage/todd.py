import logging
import subprocess

from params import todd_path, downloads_dir


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
        logging.debug(stdout)

    if len(stderr) > 0:
        logging.error(stderr)


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
        logging.debug(stdout)

    if len(stderr) > 0:
        logging.error(stderr)


if __name__ == '__main__':
    download('17gKW1EkDRosvrwmnKbz9VLpus58jiByq', downloads_dir)

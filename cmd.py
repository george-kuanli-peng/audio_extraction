import os

from util.config import config
from util.ffmpeg import extract_audio_from_video, extract_audio_segment
from util.ftp import FTPConn
from util.log import logging


LOGGER = logging.getLogger(__name__)
WORK_DIR = config.get_value('audio_video', 'work_dir')


def main():
    # TODO: 防止檔案重覆下載
    ftp_conn = FTPConn()
    rec_file_name = ftp_conn.get_latest_rec_file_name()
    LOGGER.info(f'Found latest recording file: {rec_file_name}')
    ftp_conn.download_file(rec_file_name, WORK_DIR)
    rec_main_file_name = rec_file_name.rsplit(maxsplit=1)[0]
    orig_audio_file_name = rec_main_file_name + '.aac'
    conv_audio_file_name = rec_main_file_name + '.mp3'
    LOGGER.info(f'Extracting audio to {orig_audio_file_name}...')
    extract_audio_from_video(os.path.join(WORK_DIR, rec_file_name),
                             os.path.join(WORK_DIR, orig_audio_file_name))
    LOGGER.info(f'Converting audio to {conv_audio_file_name}...')
    extract_audio_segment(os.path.join(WORK_DIR, orig_audio_file_name),
                          os.path.join(WORK_DIR, conv_audio_file_name))


if __name__ == '__main__':
    main()

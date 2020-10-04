#!/usr/bin/env python
import os
from contextlib import suppress

from util.config import config
from util.db import get_completed_video_files, get_completed_raw_audio_files, get_completed_final_audio_files, \
    add_completed_video_file, add_completed_raw_audio_file, add_completed_final_audio_file, \
    get_completed_uploaded_final_audio_files, add_completed_uploaded_final_audio_file
from util.ffmpeg import extract_audio_from_video, extract_audio_segment
from util.ftp import FTPConn
from util.log import logging

LOGGER = logging.getLogger(__name__)
WORK_DIR = config.get_value('audio_video', 'work_dir')


def main():
    ftp_conn = FTPConn()
    rec_file_name = ftp_conn.get_latest_rec_file_name()
    LOGGER.info(f'Found latest recording file: {rec_file_name}')

    rec_main_file_name = rec_file_name.rsplit(maxsplit=1)[0]
    orig_audio_file_name = rec_main_file_name + '.aac'
    conv_audio_file_name = rec_main_file_name + '.mp3'

    rec_file_path = os.path.join(WORK_DIR, rec_file_name)
    orig_audio_file_path = os.path.join(WORK_DIR, orig_audio_file_name)
    conv_audio_file_path = os.path.join(WORK_DIR, conv_audio_file_name)

    def _proc_upload_final_audio_file():
        if conv_audio_file_name in get_completed_uploaded_final_audio_files():
            LOGGER.warning(f'Final audio file {conv_audio_file_name} has been already uploaded')
            return
        _proc_conv_audio_file()
        ftp_conn.upload_file(conv_audio_file_name, WORK_DIR)
        add_completed_uploaded_final_audio_file(conv_audio_file_name)
        _cleanup_intermediate_files()

    def _proc_conv_audio_file():
        if conv_audio_file_name in get_completed_final_audio_files() and os.path.exists(conv_audio_file_path):
            LOGGER.warning(f'Final audio file {conv_audio_file_name} has been already processed')
            return
        _proc_extract_audio_file()
        LOGGER.info(f'Converting audio to {conv_audio_file_name}...')
        extract_audio_segment(orig_audio_file_path, conv_audio_file_path, output_encoder='libmp3lame',
                              start_time=config.get_value('audio_video', 'default_clip_start'),
                              stop_time=config.get_value('audio_video', 'default_clip_end'))
        add_completed_final_audio_file(conv_audio_file_name)

    def _proc_extract_audio_file():
        if orig_audio_file_name in get_completed_raw_audio_files() and os.path.exists(orig_audio_file_path):
            LOGGER.warning(f'Original audio file {orig_audio_file_name} has been extracted')
            return
        _proc_download_video_file()
        LOGGER.info(f'Extracting audio to {orig_audio_file_name}...')
        extract_audio_from_video(rec_file_path, orig_audio_file_path)
        add_completed_raw_audio_file(orig_audio_file_name)

    def _proc_download_video_file():
        if rec_main_file_name in get_completed_video_files() and os.path.exists(rec_file_path):
            LOGGER.warning(f'Original video file {rec_file_name} has been downloaded')
            return
        ftp_conn.download_file(rec_file_name, WORK_DIR)
        add_completed_video_file(rec_file_name)

    def _cleanup_intermediate_files():
        LOGGER.info(f'Cleaning up intermediate files...')
        for file_path in (rec_file_path, orig_audio_file_path):
            with suppress(FileNotFoundError):
                os.remove(file_path)

    _proc_upload_final_audio_file()


if __name__ == '__main__':
    main()

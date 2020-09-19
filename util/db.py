import os.path
from typing import List

from util.config import config


_WORK_DIR = config.get_value('audio_video', 'work_dir')
_CMPL_VIDEOS_DB_PATH = os.path.join(os.path.dirname(__file__), '..', _WORK_DIR, 'videos.txt')
_CMPL_RAW_AUDIOS_DB_PATH = os.path.join(os.path.dirname(__file__), '..', _WORK_DIR, 'raw_audios.txt')
_CMPL_FINAL_AUDIOS_DB_PATH = os.path.join(os.path.dirname(__file__), '..', _WORK_DIR, 'final_audios.txt')


def _get_local_db_recs(db_file_path: str) -> List[str]:
    try:
        with open(db_file_path, 'rt', encoding='utf8') as fd:
            return [line.strip() for line in fd.readlines() if line.strip() != '']
    except FileNotFoundError:
        return []


def _add_local_db_rec(db_file_path: str, rec: str):
    with open(db_file_path, 'at', encoding='utf8') as fd:
        fd.write('\n' + rec)


def get_completed_video_files() -> List[str]:
    return _get_local_db_recs(_CMPL_VIDEOS_DB_PATH)


def add_completed_video_file(file_name: str):
    _add_local_db_rec(_CMPL_VIDEOS_DB_PATH, file_name)


def get_completed_raw_audio_files() -> List[str]:
    return _get_local_db_recs(_CMPL_RAW_AUDIOS_DB_PATH)


def add_completed_raw_audio_file(file_name: str):
    _add_local_db_rec(_CMPL_RAW_AUDIOS_DB_PATH, file_name)


def get_completed_final_audio_files() -> List[str]:
    return _get_local_db_recs(_CMPL_FINAL_AUDIOS_DB_PATH)


def add_completed_final_audio_file(file_name: str):
    _add_local_db_rec(_CMPL_FINAL_AUDIOS_DB_PATH, file_name)

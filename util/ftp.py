import logging
import os
from datetime import date, datetime, timedelta
from ftplib import FTP
from typing import IO

from util.config import config
from util.log import *


LOGGER = logging.getLogger(__name__)


# ftp.cwd('10-大堂錄影'.encode('big5').decode('latin'))
# ret = list(ftp.mlsd())
# >>> ret
# [('.DS_Store', {'modify': '20200504024103', 'type': 'file', 'unique': '3EU190', 'size': '10244', 'unix.mode': '0777', 'unix.owner': 'worker', 'unix.group': 'users'}), ('#recycle', {'modify': '20190807033240', 'type': 'dir', 'unique': '3EU103', 'size': '246', 'unix.mode': '0000', 'unix.owner': 'root', 'unix.group': 'root'}), ('10-¤j°ó¿ý¼v', {'modify': '20200628041800', 'type': 'dir', 'unique': '3EU15E', 'size': '212', 'unix.mode': '0777', 'unix.owner': 'root', 'unix.group': 'root'}), ('10-·q«ô¹Î', {'modify': '20200504024030', 'type': 'dir', 'unique': '3EU105', 'size': '76', 'unix.mode': '0777', 'unix.owner': 'root', 'unix.group': 'root'})]
# >>> ret[2][0].encode('latin').decode('big5')
# '10-大堂錄影'


FTP_HOST = config.get_value('ftp', 'host')
FTP_USER = config.get_value('ftp', 'username')
FTP_PASS = config.get_value('ftp', 'password')
FTP_SRC_DIR = config.get_value('ftp', 'src_dir')
FTP_DST_DIR = config.get_value('ftp', 'dst_dir')
FTP_ENCODING = config.get_value('ftp', 'encoding')


class FTPConn:

    def __init__(self):
        self.ftp = FTP(FTP_HOST)
        self.ftp.login(user=FTP_USER, passwd=FTP_PASS)

    def get_file_list(self):
        self.ftp.cwd('/' + FTP_SRC_DIR.encode(FTP_ENCODING).decode('latin'))
        return list(self.ftp.mlsd())

    def get_latest_rec_file_name(self) -> str:
        cur_latest_rec_time = datetime(2000, 1, 1, 0, 0, 0)
        cur_latest_rec_file_name = None
        for f_info in reversed(self.get_file_list()):
            file_name = f_info[0]
            try:
                file_time = datetime.strptime(file_name, '%Y-%m-%d %H-%M-%S.mkv')
                if file_time > cur_latest_rec_time:
                    cur_latest_rec_time = file_time
                    cur_latest_rec_file_name = file_name
            except ValueError:
                pass
        if not cur_latest_rec_file_name:
            raise ValueError('Recording file not found')
        return cur_latest_rec_file_name

    def get_rec_file_name_for_date(self, rec_date: date) -> str:
        # LOGGER.warning(f'rec_date={rec_date}')
        for f_info in reversed(self.get_file_list()):
            file_name = f_info[0]
            try:
                file_time = datetime.strptime(file_name, '%Y-%m-%d %H-%M-%S.mkv')
                # LOGGER.warning(f'file_name={file_name}, file_time={file_time.date()}')
                if file_time.date() == rec_date:
                    return file_name
            except ValueError:
                pass
        raise ValueError('Recording file not found')

    def download_file(self, file_name: str, dst_dir: str):
        dst_file_path = os.path.join(dst_dir, file_name)
        with open(dst_file_path, 'wb') as f_store:
            self.ftp.cwd('/' + FTP_SRC_DIR.encode(FTP_ENCODING).decode('latin'))
            total_bytes = self.ftp.size(file_name)
            LOGGER.info(f'"{file_name}" download started, total {int(total_bytes/1024):,} KBytes')
            downloader = FileDownloader(f_store, total_bytes)
            self.ftp.retrbinary('RETR ' + file_name, downloader.retr)
            LOGGER.info(f'"{file_name}" download completed')

    def upload_file(self, file_name: str, local_dir: str):
        src_file_path = os.path.join(local_dir, file_name)
        with open(src_file_path, 'rb') as fd:
            self.ftp.cwd('/' + FTP_DST_DIR.encode(FTP_ENCODING).decode('latin'))
            LOGGER.info(f'"{file_name}" upload started')
            self.ftp.storbinary('STOR ' + file_name, fd)
            LOGGER.info(f'"{file_name}" upload completed')


class FileDownloader:

    def __init__(self, fp: IO, total_bytes: int):
        self.fp = fp
        self.total_bytes = total_bytes
        self.cur_bytes = 0
        self.log_cnt = 0
        self.log_interval = timedelta(seconds=10)
        self.last_log_time = datetime.now()

    def retr(self, block):
        self.cur_bytes = self.cur_bytes + len(block)
        self.fp.write(block)

        self.log_cnt = self.log_cnt + 1
        if self.log_cnt % 20 == 0:
            cur_time = datetime.now()
            if cur_time - self.last_log_time >= self.log_interval:
                cur_kbytes = int(self.cur_bytes/1024)
                cur_percent = self.cur_bytes / self.total_bytes * 100
                LOGGER.info(f'Total {cur_kbytes:,} KBytes ({cur_percent:.2f}%) downloaded')
                self.last_log_time = cur_time

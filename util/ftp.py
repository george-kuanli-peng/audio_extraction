from util.config import config
from ftplib import FTP


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
FTP_ENCODING = config.get_value('ftp', 'encoding')


class FTPConn:

    def __init__(self):
        self.ftp = FTP(FTP_HOST)
        self.ftp.login(user=FTP_USER, passwd=FTP_PASS)
        self.ftp.cwd(FTP_SRC_DIR.encode(FTP_ENCODING).decode('latin'))

    def get_file_list(self):
        return list(self.ftp.mlsd())

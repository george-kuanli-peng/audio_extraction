from ftplib import FTP
from typing import Optional


# ftp.cwd('10-大堂錄影'.encode('big5').decode('latin'))
# ret = list(ftp.mlsd())
# >>> ret
# [('.DS_Store', {'modify': '20200504024103', 'type': 'file', 'unique': '3EU190', 'size': '10244', 'unix.mode': '0777', 'unix.owner': 'worker', 'unix.group': 'users'}), ('#recycle', {'modify': '20190807033240', 'type': 'dir', 'unique': '3EU103', 'size': '246', 'unix.mode': '0000', 'unix.owner': 'root', 'unix.group': 'root'}), ('10-¤j°ó¿ý¼v', {'modify': '20200628041800', 'type': 'dir', 'unique': '3EU15E', 'size': '212', 'unix.mode': '0777', 'unix.owner': 'root', 'unix.group': 'root'}), ('10-·q«ô¹Î', {'modify': '20200504024030', 'type': 'dir', 'unique': '3EU105', 'size': '76', 'unix.mode': '0777', 'unix.owner': 'root', 'unix.group': 'root'})]
# >>> ret[2][0].encode('latin').decode('big5')
# '10-大堂錄影'


def get_file(host: str, file_path: str, encoding: Optional[str] = None,
             username: Optional[str] = None, password: Optional[str] = None):
    pass


def _get_ftp_conn(host: str, username: Optional[str] = None, password: Optional[str] = None) -> FTP:
    ftp = FTP(host)
    ftp.login(user=username, passwd=password)
    return ftp

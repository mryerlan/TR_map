import csv
from ftplib import FTP as _FTP
import contextlib


@contextlib.contextmanager
def connect_to_ftp(host, username='', password='', cd='', port=21):
    assert isinstance(host, str)
    assert isinstance(username, str)
    assert isinstance(password, str)
    assert isinstance(port, int), 'port must be an integer.'
    assert isinstance(cd, str)

    ftp = _FTP()
    try:
        ftp.connect(host, port)
        ftp.login(username, password)
        ftp.cwd(cd)
        yield ftp
    except Exception:
        raise
    finally:
        ftp.quit()


def open_file_from_ftp(ip, username, password, filename, cd):
    with connect_to_ftp(ip, username, password, cd) as ftp:
        file_ = ftp.nlst(filename)[0]
        with open(file_, "wb") as file:
            ftp.retrbinary("RETR " + file_, file.write)

    return file_

from config import AppConfig
from datetime import datetime


class Logger:

    def log(self, text):
        raise NotImplementedError


class FileLogger(Logger):

    def __init__(self):
        self.fd = None

    def init_logger(self):
        self.fd = open(AppConfig.log_file_name, 'a')

    def stop_logger(self):
        self.fd.close()

    def log(self, text):
        self.fd.write('%s: %s\n' % (str(datetime.now()), text))


file_logger = FileLogger()

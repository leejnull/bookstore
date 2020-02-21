import logging
from bookstore.settings import DEBUG


class Logger(object):

    def __init__(self):
        self.logger_debug = logging.getLogger('django')
        self.logger_release = logging.getLogger('django.request')

    def debug(self, msg, *args, **kwargs):
        if DEBUG:
            self.logger_debug.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if DEBUG:
            self.logger_debug.info(msg, *args, **kwargs)
        else:
            self.logger_release.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if DEBUG:
            self.logger_debug.warning(msg, *args, **kwargs)
        else:
            self.logger_release.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if DEBUG:
            self.logger_debug.error(msg, *args, **kwargs)
        else:
            self.logger_release.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if DEBUG:
            self.logger_debug.critical(msg, *args, **kwargs)
        else:
            self.logger_release.critical(msg, *args, **kwargs)


logger = Logger()

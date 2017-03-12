import logging
from click import style

def fmt_debug(text):    return style(text, bold=True, fg='green')
def fmt_info(text):     return style(text, bold=True)
def fmt_warn(text):     return style(text, bold=True, fg='yellow')
def fmt_error(text):    return style(text, bold=True, fg='red')

fmt_text = {
        'debug': fmt_debug,
        'info': fmt_info,
        'warn': fmt_warn,
        'error': fmt_error,
        }

def setup_custom_logger(name='debug'):
    formatter = logging.Formatter(fmt='{} [{}] {}'.format(
                style('%(asctime)s',fg='cyan'),
                fmt_text[name]('%(levelname)s'),
                '%(message)s'), 
            datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

_debug = setup_custom_logger('debug')
_info = setup_custom_logger('info')
_warn = setup_custom_logger('warn')
_error = setup_custom_logger('error')

def debug(text):    _debug.debug(text)
def info(text):     _info.info(text)
def warn(text):     _warn.warn(text)
def error(text):    _error.error(text)

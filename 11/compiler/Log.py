import logging
import colorlog
from colorlog import ColoredFormatter

log_colors_config = {
    'DEBUG': 'white',  # cyan white
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

console_formatter = ColoredFormatter(
    fmt='%(log_color)s[%(asctime)s.%(msecs)03d] -> [%(levelname)s] %(filename)s %(funcName)s (%(lineno)d) :  %(message)s',
    datefmt='%H:%M:%S',
    log_colors=log_colors_config
)

file_formatter = logging.Formatter(
    fmt='[%(asctime)s.%(msecs)03d] -> [%(levelname)s] %(filename)s %(funcName)s (%(lineno)d) :  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

console_handler = colorlog.StreamHandler()
console_handler.setFormatter(console_formatter)
file_handler = logging.FileHandler('./log.txt')
file_handler.setFormatter(file_formatter)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)







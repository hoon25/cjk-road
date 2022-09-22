import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def get_custom_logger(name):
    logger = logging.getLogger("cjk-logger")
    logger.setLevel(logging.DEBUG)

    # handler 객체 생성
    stream_handler = logging.StreamHandler()
    debug_file_handler = logging.FileHandler(filename=ROOT_DIR.joinpath('log', f"{name}-debug.log"))
    inf_file_handler = logging.FileHandler(filename=ROOT_DIR.joinpath('log', f"{name}-info.log"))
    err_file_handler = logging.FileHandler(filename=ROOT_DIR.joinpath('log', f"{name}-error.log"))

    # formatter 객체 생성
    formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # handler에 level 설정
    stream_handler.setLevel(logging.INFO)
    debug_file_handler.setLevel(logging.DEBUG)
    inf_file_handler.setLevel(logging.INFO)
    err_file_handler.setLevel(logging.ERROR)

    # handler에 format 설정
    stream_handler.setFormatter(formatter)
    debug_file_handler.setFormatter(formatter)
    inf_file_handler.setFormatter(formatter)
    err_file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(debug_file_handler)
    logger.addHandler(inf_file_handler)
    logger.addHandler(err_file_handler)

    return logger

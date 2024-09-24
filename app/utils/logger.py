# init logging
import logging

logger = logging.getLogger('uvicorn.logger')
logger.setLevel(logging.INFO)

# 콘솔 핸들러 및 포맷 설정
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def get_logger():
    return logger



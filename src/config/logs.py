import logging

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%H:%M:%S")
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.handlers.clear()
logger.addHandler(handler)
logger.propagate = False
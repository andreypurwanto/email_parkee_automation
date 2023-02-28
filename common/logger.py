import logging
# from utils.context_filter import ContextFilter

handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s %(levelname)s]%(filename)s:%(lineno)s : %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger.addFilter(ContextFilter())
logger.addHandler(handler)

LOG = logger
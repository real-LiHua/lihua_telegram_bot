import logging as __logging
from logging import INFO, WARNING

__logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO
)

__logging.getLogger("httpx").setLevel(WARNING)
log = __logging.getLogger(__name__)

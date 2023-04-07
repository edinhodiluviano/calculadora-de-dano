import logging.config

from mangum import Mangum

from service import main


logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    """Call relevant code and return status_code."""

    asgi_handler = Mangum(main.app)
    response = asgi_handler(event, context)
    return response

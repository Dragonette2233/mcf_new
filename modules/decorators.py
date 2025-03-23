import requests
import logging

logger = logging.getLogger(__name__)

class MCFDecorator:

    @staticmethod
    def connection_handler(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except (requests.exceptions.ConnectTimeout, 
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ReadTimeout):
                logger.warning("No coonection | Connection timeot")
            except Exception as exc:
                logger.error(exc, exc_info=True)
            return result
        return wrapper
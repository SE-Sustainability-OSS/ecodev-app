from time import sleep
from ecodev_core import logger_get
log=logger_get(__name__)



def wait_for_selenium(selenium_url: str, max_retries: int = 30, delay: int = 5):
    """
    Wait for Selenium service to be ready before connecting.
    """
    import requests
    url = f'{selenium_url}/status'
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                log.info(f'Selenium is ready at {url}')
                return True
        except Exception as e:
            log.info(f'Attempt {attempt + 1}/{max_retries}: Selenium not ready yet - {e}')
        sleep(delay)
    raise ConnectionError(f'Failed to connect to Selenium at {url} after {max_retries} attempts')
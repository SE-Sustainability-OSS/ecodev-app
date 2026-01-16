import logging
import os
import unittest
from time import sleep

from ecodev_core import engine
from ecodev_core import SafeTestCase
from ecodev_core import SETTINGS
from ecodev_core.app_user import USER_INSERTOR
from ecodev_core.authentication import _hash_password
from ecodev_core.db_insertion import create_or_update
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from sqlmodel import Session
from ecodev_core import logger_get

from tests_frontend.commons import wait_for_selenium
logger = logging.getLogger('selenium')
logger.setLevel(logging.DEBUG)
TIMEOUT = 20
BIG_TIMEOUT = 40
SELENIUM_URL = 'http://selenium:4444/wd/hub'
log = logger_get(__name__)
class PythonOrgSearchTest(SafeTestCase):
    @classmethod
    def setUpClass(cls):
        """
        To run this test locally, set environment variable SELENIUM_LOCAL=true
        """
        super().setUpClass()
        log.info('starting driver')
        cls.create_test_db()
        options = webdriver.ChromeOptions()
        
        wait_for_selenium(SELENIUM_URL)
        cls.driver = webdriver.Remote(command_executor=SELENIUM_URL,
                                      options=options)

        log.info('starting browser')
        with Session(engine) as session:
            session.add(create_or_update(session,
                                         {'id': None,
                                          'user': SETTINGS.api.user,
                                          'password': _hash_password(SETTINGS.api.password),
                                          'permission': 'Consultant',
                                          'client': 'project_name',
                                          'application': 'application_name'
                                          }, USER_INSERTOR))
        cls.driver.get('http://ecodev_app:80')
        log.info('starting tests')

    @classmethod
    def tearDownClass(cls):
        cls.delete_test_db()
        cls.driver.quit()
        return super().tearDownClass()

    def setUp(self):
        return super().setUp(handle_db=False)

    def tearDown(self):
        return super().tearDown(handle_db=False)

    def test_connection(self):
        """
        Test that we can properly connect to the app
        
        new_project_button = WebDriverWait(self.driver, TIMEOUT).until( will throw an error if the
        button is not visible in the app, therefore ending the test without error means we logged
        properly
        """
        log.info('logging in')
        login_field = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='{\"index\":\"username\",\"type\":\"login\"}']")))
        login_field.send_keys(SETTINGS.api.user)
        password_field = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='{\"index\":\"password\",\"type\":\"login\"}']")))
        password_field.send_keys(SETTINGS.api.password)
        sleep(1)
        self.driver.find_element(
            By.XPATH, "//button[@id='{\"index\":\"button\",\"type\":\"login\"}']").click()

        new_project_button = WebDriverWait(self.driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='{\"index\":\"new-project-button-id\",\"type\":\"module-button\"}']")))
        log.info('login successfull')







if __name__ == '__main__':

    unittest.main()
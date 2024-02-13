import unittest
import requests
import time

# selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


class InputTests(unittest.TestCase):

    def send_request(self, test_input):
        self.driver.get(self.APP_ADDR)
        # find location search input bar and send request
        location_input = self.driver.find_element(By.NAME, "city_country")
        location_input.send_keys(test_input)
        location_input.send_keys(Keys.RETURN)

    def setUp(self):
        ip = requests.get('https://api.ipify.org').content.decode('utf8')
        self.APP_ADDR = f"http://{ip}/home"
        self.TEST_LOCATION = "London"
        self.BAD_INPUT = "kasdjh92834reghiuroo34234"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=self.options)

    def test_connection(self):
        """Asserts a 200 response code from the weather web app using requests module"""

        response = requests.get(self.APP_ADDR, timeout=7).status_code
        self.assertEqual(response, 200, "Web app is not reachable")

    def test_positive(self):
        """Asserts a response page has loaded for a good location input"""
        self.send_request(self.TEST_LOCATION)

        # wait for location search response
        time.sleep(1.5)

        # If location is good it will appear in title
        result_title = self.driver.current_url
        self.assertIn(self.TEST_LOCATION, result_title, "Possitive input test - not passed")
        self.driver.close()

    def test_negative(self):
        """Assert that a wrong location input returns to home"""
        self.send_request(self.BAD_INPUT)

        # wait for location search response
        time.sleep(1.5)

        result_title = self.driver.current_url
        self.assertIn("home", result_title, "Negative input test - not passed")
        self.driver.close()

    def tearDown(self) -> None:
        return None


if __name__ == "__main__":
    unittest.main()

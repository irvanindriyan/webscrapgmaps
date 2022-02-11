#config in app.py
#run run.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from time import sleep, strftime, localtime
import app, csv

class WebDriver():
    def __init__(self, debug):
        self.debug = debug
        service = Service(executable_path=app.browserPath)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()

    def _log(self, info):
        if self.debug:
            with open(app.logFile, 'a', encoding='utf-8') as file:
                info = strftime('[%d-%m-%Y %H:%M:%S]: ', localtime())+info
                file.writelines(info+'\n')

    def _get_url(self):
        return self.driver.current_url

    def _get_element(self, xpath):
        try:
            element = WebDriverWait(self.driver, app.timeOut).until(
                expected_conditions.visibility_of_element_located(
                    (By.XPATH, xpath)
                )
            )
        except TimeoutException:
            return None
        return element

    def _get_text(self, xpath):
        if (e := self._get_element(xpath)) is not None and e.text != '':
            return str(e.text)
        return ''

    def _get_number(self, xpath):
        if (e := self._get_element(xpath)) is not None and e.text != '':
            return str(e.text).replace(',', '.')
        return 0

    def _click_element(self, ele):
        try:
            self._get_element(ele).click()
            sleep(app.timeOut)
        except AttributeError:
            return False
        return True

    def _click_js(self, xpath, disabled=False):
        try:
            element = self._get_element(xpath)
            sleep(app.timeOut)
            id = element.get_attribute('id')
            if disabled:
                self.driver.execute_script(
                    f'document.querySelector(\'#{id}\').disabled = false;'
                )
                sleep(app.timeOut)
            self.driver.execute_script(
                f'document.querySelector(\'#{id}\').click();'
            )
            sleep(app.timeOut)
        except Exception:
            return False
        return True

    def quit(self):
        self._log('Close browser >')
        self.driver.close()

class GoogleMapsScraper(WebDriver):
    def __init__(self, debug=False):
        super().__init__(debug)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.quit()

    def _get_text_js(self, src):
        try:
            text = self.driver.execute_script(
                f'return document.querySelector("img[src*={src}]")'
                '.parentNode.parentNode.parentNode.children[1].innerText;'
            )
            if 'Add' in text or text == '':
                return ''
            return text
        except Exception:
            return ''

    def search_query(self, searchText):
        self.driver.get(app.baseUrl+searchText)
        self._log('Search place from URL > '+searchText)
        sleep(app.waitTime)

    def identify_url(self):
        return self._get_url().split('/')[4]

    def write_data(self, data, fileName):
        with open(fileName, 'a', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            self._log('Writing log > '+str(data[:3]))
            csvwriter.writerow(data)

    def get_place_data(self, fileName):
        name = self._get_text(app.placeName)
        address = self._get_text_js(app.placeAddress)
        pluscode = self._get_text_js(app.placeCode).split(', ')
        if len(pluscode) > 1:
            provincy = pluscode[-1]
            region = pluscode[-2]
        else:
            provincy = ''
            region = ''
        pos = address.split(' ')[-1]
        contact = self._get_text_js(app.placeContact)
        website = self._get_text_js(app.placeWebsite)
        rating = self._get_number(app.placeRating)
        review = self._get_text(app.placeReview)

        url = self._get_url()
        result = [
            name, address, region, provincy, pos, contact, '', website, rating, review
        ]
        self.write_data(result, fileName)

    def _next_page(self, prev):
        try:
            self._click_element(app.backButton)
            self._click_js(app.nextPage, True)
            if (e := self._get_element(app.firstResult)) != prev:
                e.click()
            else:
                return False
        except Exception:
            return False
        return e

    def get_places_data(self, fileName, queryLen):
        self._click_element(app.firstResult)
        results_found, prev = 1, None
        rn = 6
        while results_found <= queryLen:
            if (results_found % rn) == 0:
                rn = 5
                self._click_element(app.nextPane)
            
            if (rf := results_found % 20) == 0:
                if not self._click_element(app.bottomPane+'[20]'):
                    break
                self.get_place_data(fileName)
                if not (prev := self._next_page(prev)):
                    break
            else:
                if not self._click_element(app.bottomPane+f'[{rf}]'):
                    break
                self.get_place_data(fileName)
            results_found += 1

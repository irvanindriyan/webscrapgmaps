# Web Scrap
Google Maps with Python

#Required
- from selenium import webdriver
- from selenium.webdriver.chrome.service import Service
- from selenium.webdriver.common.by import By
- from selenium.webdriver.support.ui import WebDriverWait
- from selenium.webdriver.support import expected_conditions
- from selenium.common.exceptions import TimeoutException
- from time import sleep, strftime, localtime
- from mapsscrapping import GoogleMapsScraper
- from win10toast import ToastNotifier
- import csv
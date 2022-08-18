import os
import re
import furl
import time
import codecs
import requests

from unipath import Path
from bs4 import BeautifulSoup

from tldextract import extract
from urllib.parse import urlparse, urljoin
from urllib.request import Request, urlopen

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

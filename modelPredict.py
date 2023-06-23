# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 01:57:41 2023

@author: chuns
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs
import re as re
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Edge()

text = 'only answer yes or no Is this job fit for new graduate student: 3+ years of hands-on experience developing single page web applications and writing JavaScript/Typescript, HTML, CSS\
Mastered understanding of software tools and the ability to be a conduit between engineering/client leadership and engineering direction\
Experience with React.js and strong component-based design involvement\
Experience writing data driven tests, mocking, and unit tests in each layer\
Experience cloning, branching, committing, and submitting pull requests with Git\
Experience coding microservices (any language) '

edgeUrl = "https://www.bing.com/search?form=MW00X7&pl=launch&q=Bing+AI&showconv=1&sydconv=1"
driver.get(edgeUrl)
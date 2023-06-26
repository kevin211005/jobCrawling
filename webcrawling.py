# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 22:49:37 2023

@author: chuns
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from datetime import date
import re 
linkedInLogInUrl = "https://www.linkedin.com/uas/login"
PeriodTable = {"0": "", "1":"&f_TPR=r2592000", "2":"&f_TPR=r604800", "3":"&f_TPR=r86400"}
JobSearchUrl = "https://www.linkedin.com/jobs/search/?"
class webcrawling:
    def __init__(self, max_wait_time = 5):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, max_wait_time)
        self.max_wait_time = max_wait_time
    def logIn(self, userName, password):
        self.driver.get(linkedInLogInUrl)
        time.sleep(1)
        email = self.driver.find_element(By.ID, 'username')
        email.send_keys(userName)
        passwordElement = self.driver.find_element(By.ID, 'password')
        passwordElement.send_keys(password)
        passwordElement.send_keys(Keys.RETURN)  
    def getJobs(self, timePeriod, keyword, location, workYrs,test = False):
        keyword = "&keywords=" + keyword.lower().replace(" ", "%20") 
        keyword = keyword + "&location=" + location.lower().replace(" ", "%20").replace(",", "%2C").capitalize() if len(location) != 0 else keyword
        period = PeriodTable[timePeriod]
        jobPostURL = JobSearchUrl + period + keyword
        self.driver.get(jobPostURL)
        time.sleep(3)
        barClassName = "artdeco-pagination__pages.artdeco-pagination__pages--number"
        try:
            changePageBar = self.driver.find_element(By.CLASS_NAME, barClassName)
            buttons = changePageBar.find_elements(By.TAG_NAME, 'button')
            # Get number of pages 
            lastPage = 0 
            attempts = 0 
            while attempts <= 2:
                try:
                    lastPage = int(buttons[-1].text)
                    break 
                except:
                    attempts += 1 
            JobsInfo = []
            ###test mode only check 3 pages 
            if test == True:
                lastPage = 3
            for index in range(2, lastPage + 1):
                singleJobInfo = self.getSinglePageJobPost()
                JobsInfo += singleJobInfo
                if len(singleJobInfo) < 20:
                    print(f"Error occur on page {index - 1}")
                cssSelector = f'li[data-test-pagination-page-btn="{index}"]'
                button = changePageBar.find_elements(By.CSS_SELECTOR, cssSelector)
                if len(button) == 1:
                    button[0].click()
                else:
                    button = changePageBar.find_elements(By.TAG_NAME, "button")[-2]
                attempts = 0 
                while attempts <= 2:
                    try:
                        print(button.text)
                        button.click()
                        break 
                    except:
                        attempts += 1 
            print("Total Job get from webcrawling:", len(JobsInfo))
            df = pd.DataFrame(JobsInfo)
            df_unique = df.drop_duplicates(subset=['id'])
            data = df_unique.to_dict('records')
            print(f"Find {len(data)} unique jobs")
            jobSelected, citizenJobs = self.filterData(data, workYrs)
            print(f"find {len(jobSelected)} jobs for you and {len(citizenJobs)} jobs for us citizen only")
            return jobSelected
        except Exception as e:
            print("Get page number error")
            print(e)
            return None 
    def findJobList(self, className):
        joblist = None
        try:
            joblist = self.wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, className)))
            print(f"Find {len(joblist)} jobs in this page")
        except:
            print("Loading Job list error")
        return joblist
    def loadContent(self, jobInfo):
        errorCount = 0 
        className = "ember-view.jobs-search-results__list-item.occludable-update.p0.relative.scaffold-layout__list-item"
        titleClass = "t-24.t-bold.jobs-unified-top-card__job-title"
        companyClass = "ember-view.t-black.t-normal"
        jobContentClass = "jobs-box__html-content.jobs-description-content__text.t-14.t-normal.jobs-description-content__text--stretch"
        joblist = self.findJobList(className)
        if joblist == None:
            errorCount = 25
        for job in joblist:
            try:
                job.click()
                job.click()
                # Wait until the element appears
                titleElement = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, titleClass)))
                companyElement = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, companyClass)))
                parentElement = self.driver.find_element(By.CLASS_NAME, jobContentClass)
                spanElement = WebDriverWait(parentElement, self.max_wait_time).until(EC.visibility_of_element_located((By.TAG_NAME, "span")))
                content = self.lowercaseAndRemoveSpace(spanElement.text) 
                postInfo = {}
                postInfo["jobTitle"] = titleElement.text  
                postInfo["company"] = companyElement.text
                postInfo["id"] = postInfo["jobTitle"] + " " + postInfo["company"] 
                postInfo["description"] = content
                postInfo["url"] = self.driver.current_url
                jobInfo.append(postInfo)
            except StaleElementReferenceException:
                errorCount += 1
                print("StaleElementReferenceException")
                pass
            except TimeoutException:
                print("TimeOut try again to get job content")
                errorCount += 1
                pass  
            except Exception as e:
                print("Uncatched exception occured")
                print(e)
                errorCount += 1
                pass  
        print("error count = ", errorCount)
        return errorCount
    def close(self):
        self.driver.close()
    #get single page job post 
    def getSinglePageJobPost(self):
        jobInfo = []
        errorCount = self.loadContent(jobInfo)
        #retry when error count greater than 20 
        if(errorCount > 20):
            print("Get Page error Retry start")
            errorCount = self.loadContent(jobInfo)
        return jobInfo
    #%% data postprocess 
    def filterData(self, jobList, workYrs):
        jobSelected = []
        jobRequiredCitizenship = []
        for job in jobList:
            content = job["description"]
            if not self.isForEntryLevel(job["jobTitle"]):
                continue 
            if self.requireCitizenship(content) == True:
                jobRequiredCitizenship.append(job)
            else:
                if self.isFit(content, workYrs) == True:
                    job["date"] = str(date.today())
                    jobSelected.append(job)
        return jobSelected, jobRequiredCitizenship
    # lowercase and remove empty cols of string 
    def lowercaseAndRemoveSpace(self, content):
        lines = content.split('\n')
        non_empty_lines = [line for line in lines if line.strip()] 
        newContent = '\n'.join(non_empty_lines).lower()
        return newContent
    def isForEntryLevel(self, content):
        excludeLevels = {"Senior", "Principal", "Staff", "Lead", "Sr", "III", "Mid-Level", "Mid Level"}
        return not self.contains(content, excludeLevels) 
    def requireCitizenship(self, content):
        usCitizenSet = {"u.s. citizen", "green card", "u.s person", "u.s. person", "us citizen", "permanent resident", "security clearance", "u.s. citizenship", "secret clearance"}
        return self.contains(content, usCitizenSet) 
    def findLinesWithKeyword(self, text, keywords):
        lines = text.split('\n')  # Split the text into lines
        linesWithKeyword = []
        for line in lines:
            if self.contains(line, keywords):
                linesWithKeyword.append(line)
        return "\n".join(linesWithKeyword)
    def isFit(self, content, workYrs):
        keywords = {"years", "yrs", "year"}
        ## extract string with keywords to determine matchness 
        newString = self.findLinesWithKeyword(content, keywords)
        ## no work experience required
        if newString == "":
            return True 
        else:
            ## require certain years of work exp, determine user yoe match 
            return self.filterExp(newString, workYrs) or "zero" in newString
    def filterExp(self, content, workYrs):
        numbersInContent = [int(num) for num in re.findall(r'\d+', content) if num != "000"]
        numbersInContent.sort()
        if len(numbersInContent) > 0:
            ##remove case that number no for years of work experience
            if numbersInContent[0] >= 15:
                return True 
            return numbersInContent[0] <= workYrs
        else:
            return True  
    def contains(self, content, keywords):
        for keyword in keywords:
            if keyword in content:
                return True 
        return False     













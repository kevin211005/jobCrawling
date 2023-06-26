# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:40:42 2023

@author: chuns
"""
from webcrawling import webcrawling
from database import databaseHandler
import getpass
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    success = False 
    quite = False 
    logIn = False 
    webCrawling = webcrawling()
    load_dotenv()
    userName = os.getenv("LINKEDIN_USERNAME")
    password = os.getenv("LINKEDIN_PASSWORD")
    datePosted = os.getenv("DATE_POSTED")
    jobName = os.getenv("JOB_NAME")
    try:
        workyoe = int(os.getenv("WORK_YOE"))
    except Exception as e:
        workyoe = None
        print(e)
    location = os.getenv("JOB_LOCATION")
    ###login Section 
    while success == False:    
        if userName == None or password == None:
            userName = input("Enter your LinkedIn userName: ")
            password = getpass.getpass("Enter your LinkedIn password: ", stream=None)
        webCrawling.logIn(userName, password)
        successString = input("Login success? Enter y or n to continue: ")      
        if successString.lower()[0] == "y":
            success = True
        else:
            userName = None
            password = None
    ###search section
    while quite == False:
        if jobName == None:
            jobName = input("Enter job name you want to search: ").strip()
        if location == None:
            location = input("Enter location you want to search(Press Enter if want search all): ").strip()
        success = False 
        if datePosted == None:
            while success == False:
                datePosted = input("Enter Date Posted for your search 0 => all, 1 => 1 month, 2 => 1 weeek, 3 => 24 hr: ")
                if datePosted in {"0","1", "2","3"}:
                    success = True 
        success = False 
        if workyoe == None:
            while success == False:
                workyoe = input("How many years of work experience do you have(Press Enter if you want find all else input number): ")
                try:
                    if(len(workyoe) == 0):
                        workYrs = 99
                    success = True 
                    workyoe = int(workyoe)
                except:
                    print("Please input valid years of experience")
        database = databaseHandler(workyoe)
        SelectedjobList = webCrawling.getJobs(datePosted, jobName, location, workyoe, test = True)
        if SelectedjobList != None:
            database.addNewData(SelectedjobList)
        stop = input("Stop? Enter s to stop, n to start new search else continue with orignal para: ")
        if len(stop) != 0 and stop.strip().lower()[0] == "s":
            quite = True 
        elif len(stop) != 0 and stop.strip().lower()[0] == "n":
            jobName = None
            location = None
            datePosted = None
            workyoe = None
    webCrawling.close()
    
        
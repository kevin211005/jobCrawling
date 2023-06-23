# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 23:40:42 2023

@author: chuns
"""
from webcrawling import webcrawling
from database import databaseHandler
import getpass
if __name__ == "__main__":
    success = False 
    quite = False 
    logIn = False 
    webCrawling = webcrawling()
    while quite == False:
        success = False 
        while success == False:    
            if logIn == False:
                userName = input("Enter your LinkedIn userName: ")
                password = getpass.getpass("Enter your LinkedIn password: ", stream=None)
                webCrawling.logIn(userName, password)
                successString = input("Login success? Enter y or n to continue: ")      
            if successString.lower()[0] == "y":
                success = True
                logIn = True 
        keyword = input("Enter jobs name you want to search: ").strip()
        success = False 
        while success == False:
            period = input("Enter Publication Date for your search 0 => all, 1 => 1 month, 2 => 1 weeek, 3 => 24 hr: ")
            if period in {"0","1", "2","3"}:
                success = True 
        success = False 
        while success == False:
            workYrs = input("How many years of work experiece do you have(Press Enter if you want find all else input number): ")
            try:
                if(len(workYrs) == 0):
                    workYrs = 99
                workYrs = int(workYrs)
                database = databaseHandler(workYrs)
                success = True 
            except:
                print("Please input valid years of experience")
        jobListForNewGrad = webCrawling.getJobs(period, keyword, workYrs, test = False)
        database.addNewData(jobListForNewGrad)
        stop = input("Stop? Enter s to stop, other press enter to continue: ")
        if len(stop) != 0 and stop.strip().lower()[0] == "s":
            quite = True 
    webCrawling.close()
    
        
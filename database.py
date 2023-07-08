# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:09:09 2023

@author: chuns
"""
import pandas as pd 
class databaseHandler:
    def __init__(self, workYears = 0):
        self.workYears = str(workYears) + "wyrs"
        self.database = self.loadData() 
        self.preLen = len(self.database)
    def loadData(self):
        try:
            database = pd.read_csv(f"data_{self.workYears}.csv", encoding='latin-1', on_bad_lines='skip')
            print("Load previous data success")
        except:
            print("No previous search records")
            database = pd.DataFrame() 
        return database
    def addNewData(self, data): 
        newDataFrame = pd.DataFrame(data)
        # try:
        #     newDataFrame = newDataFrame.drop('description', axis = 1)
        # except:
        #     print("Remove description error")
        dfCombined = pd.concat([self.database, newDataFrame]).drop_duplicates(subset="id")
        self.database = dfCombined
        if len(self.database) == self.preLen:
            print("Oops, No new opportunities found")
        else:
            print(f"Congrat you find {len(self.database) - self.preLen} new opportunities")
        try:
            self.database = self.database.sort_values(['date', 'jobTitle'], ascending=False)
            self.database.to_csv(f"data_{self.workYears}.csv", index=False)
            print("Successfully save data to csv")
            return True 
        except:
            print("Save data to csv failed, check if data.csv open?")
            return False 


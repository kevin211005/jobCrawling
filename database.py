# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 00:09:09 2023

@author: chuns
"""
from webcrawling import webcrawling
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
        except Exception as e:
            print("No previous search records")
            print(e)
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
        print(f"Congrat you find {len(self.database) - self.preLen} new opportunities")
        try:
            self.database = self.database.sort_values(['date', 'jobTitle'], ascending=False)
            self.database.to_csv(f"data_{self.workYears}.csv", index=False)
            print("Successfully save data to csv")
            return True 
        except:
            print("Save data to csv failed, check if data.csv open?")
            return False 
#%%
# if __name__ == "__main__":
# #     import re 
#     # handler = databaseHandler(0)
#     data = handler.database
#     data.loc[:10,'date'] = "2023-06-23"
#     data = data.sort_values(['date', 'jobTitle'], ascending=False)
#     dataList = data.to_dict(orient='records')
#     def contains(content, keywords):
#         for keyword in keywords:
#             if keyword in content:
#                 return True 
#         return False  
#     def find_lines_with_keyword(text, keyword):
#         lines = text.split('\n')  # Split the text into lines
#         lines_with_keyword = []
#         for line in lines:
#             if keyword in line:
#                 lines_with_keyword.append(line)
#         return "\n".join(lines_with_keyword)
# #%%
#     jobsContentWithYearsKeyWord = []
#     jobInfo = []
#     for job in dataList:
#         newString = find_lines_with_keyword(job["description"], "years")
#         if newString != "":
#             jobsContentWithYearsKeyWord.append(newString)
#             jobInfo.append(job)
#     jobsDigit = []
#     for content in jobsContentWithYearsKeyWord:
#         numbersInContent = [int(num) for num in re.findall(r'\d+', content)]
#         numbersInContent.sort()
#         if len(numbersInContent) > 0:
#             jobsDigit.append(numbersInContent)
#     print(f"{len(jobsContentWithYearsKeyWord)} contain years, {len(jobsDigit)} contained numbers")

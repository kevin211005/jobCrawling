# LinkedIn Job Crawling 

## Goal
Developed the customized job search filter web crawling for LinkedIn job posts

## Installation
```bash
#install pandas 
pip install pandas
#install selenium 
pip install selenium
```
## Create default search parameters(Optional)
```bash
touch .env file 
##Inside your .env file type
LINKEDIN_USERNAME="Your LinkedIn account"
LINKEDIN_PASSWORD="Your LinkedIn account"
DATE_POSTED="3" ##0 => all, 1 => 1 month, 2 => 1 weeek, 3 => 24 hr
JOB_NAME="Software Engineer"
WORK_YOE="0"
```
## Run 
```bash
python main.py 
```
## Demo Video 

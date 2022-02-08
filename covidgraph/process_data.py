import requests_cache
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import os
import csv
import time
from datetime import datetime
from dateutil import parser
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Define headers
header_by_day = ["#","Date","Country,Other","TotalCases","NewCases","TotalDeaths","NewDeaths","TotalRecovered","NewRecovered",
"ActiveCases","Serious,Critical","Tot Cases/1M pop","Deaths/1M pop","TotalTests","Tests/1M pop","Population","Continent"]

header_by_week = ["#", "Country,Other", "Cases in the last 7 days", "Cases in the preceding 7 days", 
"Weekly case /%/ change", "Cases in the last 7 days/1M pop", "Deaths in the last 7 days", 
"Deaths in the preceding 7 days", "Weekly Death /%/ change", "Deaths in the last 7 days/1M pop", "Population", "Continent"]

#Install driver to get links
requests_cache.install_cache('demo_cache',expire_after=None,allowable_methods=['GET'])

def split_list(a_list):
    #The number of countries is steady
    return a_list[:226], a_list[226:]

def get_time():
    #Get date
    today = date.today()
    yesterday = (today - timedelta(1)).strftime("%d-%m-%Y")
    two_days_ago = (today - timedelta(2)).strftime("%d-%m-%Y")
    now = datetime.now()
    cur_time = int(now.strftime('%H'))
    return cur_time,yesterday,two_days_ago

def add_date(rows_yesterday,rows_two_days_ago,yesterday,two_days_ago):
    #Add date to data
    for row in rows_yesterday:
        row.insert(1,yesterday)
    for row in rows_two_days_ago:
        row.insert(1,two_days_ago)
    return rows_yesterday,rows_two_days_ago

def get_innerText(row_total):
    rows_today = []
    rows_past = []
    rows_past_modify = []
    count = 0
    row_count = 224
    for n in row_total:
        n = n.get_attribute('innerText')
        if count == row_count:
            rows_past.append(n.split("\n"))
        else:
            rows_today.append(n.split("\t"))
            count+=1
    for n in rows_past:
        n.pop(0)
        n = n[: len(n) - 6]
        rows_past_modify.append(n)

    return rows_past_modify

def hotfix_data(rows_yesterday,covid_data):
    for i in covid_data:
        if len(i) != len(header_by_day):
            print("Error Header in #",i[0],i[2])
            print("Trying to fix...")
            time.sleep(3)
            i.pop(-1)
    return rows_yesterday,covid_data

def get_day_data(driver):
    row_total = driver.find_elements(By.XPATH,"//tr[@class='even'] | //tr[@class='odd']")
    
    rows_yesterday = []
    rows_two_days_ago = []

    rows_past_modify = get_innerText(row_total)

    #Split data to yesterday and two days ago
    rows_yesterday,rows_two_days_ago = split_list(rows_past_modify)
    rows_yesterday.pop(0)
    
    cur_time,yesterday,two_days_ago = get_time()

    rows_yesterday,rows_two_days_ago = add_date(rows_yesterday,rows_two_days_ago,yesterday,two_days_ago)

    covid_data = rows_two_days_ago + rows_yesterday

    #Get hotfix to ensure workflow
    rows_yesterday,covid_data = hotfix_data(rows_yesterday, covid_data)

    return rows_yesterday, covid_data


def crawl_day_covid_data():

    driver = webdriver.Chrome(ChromeDriverManager().install())
    link = "https://www.worldometers.info/coronavirus/"
    driver.get(link)
    rows_yesterday, covid_data = get_day_data(driver)

    filepath = os.getcwd() + '\covidgraph\covid-data-test\Corona_by_day.tsv'

    #If file hasn't created, it will take covid_data including yesterday and two_days_ago
    if not os.path.isfile(filepath):
        print(True)
        df_covid = pd.DataFrame(data=covid_data,columns=header_by_day)
        df_covid.to_csv(filepath, sep = "\t", mode = "a", index = False)

    #If file is there, it will take only rows_yesterday as df
    else:
        print(False)
        df_covid = pd.DataFrame(data=rows_yesterday,columns=header_by_day)
        df_covid.to_csv(filepath, sep = "\t", mode = "a", index = False,header=False)

def crawl_week_covid_data():

    driver = webdriver.Chrome(ChromeDriverManager().install())
    link = "https://www.worldometers.info/coronavirus/weekly-trends/#weekly_table"
    driver.get(link)
    row_total = driver.find_elements(By.XPATH,"//tr[@class='even'] | //tr[@class='odd']")
    row_week_trend = []
    filepath = 'covid-data-test/Corona_by_week.tsv'

    for n in row_total:
        n = n.get_attribute('textContent').split("\n")
        n[:] = [x.strip() for x in n if x.strip()]
        row_week_trend.append(n)

    df_covid_by_week = pd.DataFrame(data=row_week_trend,columns=header_by_week)
    print(df_covid_by_week)
    #df_covid_by_week.to_csv(filepath, sep = "\t", mode = "w", index = False)

crawl_day_covid_data()

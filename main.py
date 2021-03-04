# -*- coding: utf-8 -*-
import requests 
from bs4 import BeautifulSoup as BS
import sqlite3


def corona_statistics():

    #import date and time module
    from datetime import datetime
    dtime =datetime.now()

    # start parsing 
    result = requests.get("https://www.worldometers.info/coronavirus/country/georgia/")
    soup = BS(result.text, "lxml")
    
    # colect data
    new_cases= int(soup.select(".news_li strong")[0].getText().split()[0])
    new_deaths= int(soup.select(".news_li strong")[1].getText().split()[0])
    total_deaths = int(soup.select(".maincounter-number span")[1].getText().replace(",","").replace(" ",""))
    total_corona_cases=int(soup.select(".maincounter-number  span")[0].getText().replace(",","").replace(" ",""))
    total_cured = int(soup.select(".maincounter-number span")[2].getText().replace(",","").replace(" ",""))
    active_cases = total_corona_cases - total_cured - total_deaths

    
    conn = sqlite3.connect('coronadata.dt')
    c = conn.cursor()
    # create query
    c.execute("SELECT rowid, date FROM stats ORDER BY 1 DESC LIMIT 1")
    #export list data
    data_list = c.fetchall()
    conn.commit()
    conn.close()
    # change database data 
    if int(dtime.strftime("%H")) >= 9:
        
        if data_list[0][1]!=dtime.strftime("%x"):
            conn = sqlite3.connect('coronadata.dt')
            c = conn.cursor()
            c.execute("""INSERT INTO stats VALUES(?,?,?,?,?,?,?)""" ,
            (dtime.strftime("%x"),new_cases,new_deaths, active_cases,total_corona_cases,total_cured,total_deaths))
            conn.commit()
            conn.close()
    return new_cases, new_deaths, active_cases, total_corona_cases, total_cured, total_deaths

new_cases, new_deaths, active_cases, total_corona_cases, total_cured, total_deaths = corona_statistics()



#second function for printing
def print_data():
    from datetime import datetime
    dtime =datetime.now()
    print()
    print(dtime.strftime("%w %B %Y ამ დროის მონაცემებით შედეგები ასეთია: \n"))
    print(f"* მთლიანობაში დაღუპულია {total_deaths:,} ადამიანი {total_corona_cases:,} შემთხვევიდან. \nსიკვდილიანობის პროცენტული მაჩვენებელი არის {total_deaths / total_corona_cases :.2%}. \n")
    print(f"* გამოჯანმრთელებულია {total_cured:,} ადამიანი რაც არის {total_cured/ (total_corona_cases) :.2%}.\n" )
    print(f"* ამჟამად მკურნალობას გადის {active_cases:,} დაავადებულების {active_cases/ total_corona_cases:.2%}.\n")
    print(f"* დღევანდელი მონაცემებით გვაქვს დაინფიცირების {new_cases}.\n")# შემთხვევა რაც არის {new_cases/highest_daily_case :.2%}\nმაქსიმალური დაინფიცირების მაჩვენებლისა რომელიც იყო {highest_daily_case}, გასული წლის 5 დეკემბერს."))
    print(f"* დღევანდელი რიცხვი სიკვდილიანობისა არის {new_deaths}.\n") #\nრაც მაქსიმალური დღიური სიკვდილიანობის მაჩვენებლის {new_death/highest_daily_death :.2%} არის. \nმაქსიმალური იყო {highest_daily_death}.")
    print("* როგორც ამ მონაცემებიდან ვხედავთ საკმაოდ პოზიტიურად მივდივართ.")# ბოლო 1 თვეა, რიცხვები იკლებს.


# export data from database into lists 
conn = sqlite3.connect('coronadata.dt')
c = conn.cursor()

c.execute("SELECT rowid FROM stats")
r=[i[0] for i in c.fetchall()]
c.execute("SELECT date FROM stats")
d=[i[0] for i in  c.fetchall()]
c.execute("SELECT new_cases FROM stats")
nc = [i[0] for i in  c.fetchall()]
c.execute("SELECT new_deaths FROM stats")
nd = [i[0] for i in  c.fetchall()]
c.execute("SELECT active_cases FROM stats")
ac =[i[0] for i in  c.fetchall()]
c.execute("SELECT total_corona_cases FROM stats")
tcc = [i[0] for i in  c.fetchall()]
c.execute("SELECT total_cured FROM stats")
tc= [i[0] for i in  c.fetchall()]
c.execute("SELECT total_deaths FROM stats")
td = [i[0] for i in  c.fetchall()]

conn.commit()
conn.close()

# creating list of lists and list of keys for dictionary 
my_data_list = [r,d,nc,nd,ac,tcc,tc,td]
keys = ['id','date', 'new_case', 'new_death', 'active_case', 'total_corona_case', 'total_cured','total_deaths']

#importing pandas for DataFrame
import pandas as pd
from pandas import DataFrame
# creating DataFrame and printing
my_data_frame = DataFrame(dict(zip(keys,my_data_list)))
print("\n",my_data_frame)


if __name__=="__main__":
    corona_statistics()
    print_data()

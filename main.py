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
    
    # connect and create cursor
    #conn = sqlite3.connect('coronadata.dt')
    #c = conn.cursor()
    
    #create table
    """c.execute('''CREATE TABLE stats(
    date STRING, 
    new_cases INTEGER, 
    new_deaths INTEGER, 
    active_cases INTEGER, 
    total_corona_cases INTEGER,
    total_cured INTEGER,
    total_deaths INTEGER)
    
    ''');"""
    
    
    #c.execute("""
    #INSERT INTO stats VALUES (
    # ('12/05/20', 5450, 37, 0, 158154, 0, 1462))
    #('19/05/20', 2904, 53, 0, 206907, 0, 2055)""")
    
    

    
    new_cases= int(soup.select(".news_li strong")[0].getText().split()[0])
    new_deaths= int(soup.select(".news_li strong")[1].getText().split()[0])
    total_deaths = int(soup.select(".maincounter-number span")[1].getText().replace(",","").replace(" ",""))
    total_corona_cases=int(soup.select(".maincounter-number  span")[0].getText().replace(",","").replace(" ",""))
    total_cured = int(soup.select(".maincounter-number span")[2].getText().replace(",","").replace(" ",""))
    active_cases = total_corona_cases - total_cured - total_deaths

    
    conn = sqlite3.connect('coronadata.dt')
    c = conn.cursor()
    # create query
    #c.execute(""" SELECT * from stats""")
    c.execute("SELECT rowid, date FROM stats ORDER BY 1 DESC LIMIT 1")
    #export list data
    data_list = c.fetchall()
    conn.commit()
    conn.close()
    #for i in data_list:
    #    print(i)
    #print(data_list[0][1])
    # insert new data in database  after 12:00 pm
    if int(dtime.strftime("%H")) >= 9:
        #conn = sqlite3.connect('coronadata.dt')
        #c = conn.cursor()
        #for d in data_list:
        #    if d[0] !=dtime.strftime("%x"):
        #        conn = sqlite3.connect('coronadata.dt')
        #        c = conn.cursor()
        #        c.execute("""INSERT INTO stats VALUES(?,?,?,?,?,?,?)""" ,
        #        (dtime.strftime("%x"),new_cases,new_deaths, active_cases,total_corona_cases,total_cured,total_deaths))
        #        #break
        #        conn.commit()
        #        conn.close()
        #for i in data_list:
            #if i !=dtime.strftime("%x"):
        if data_list[0][1]!=dtime.strftime("%x"):
            conn = sqlite3.connect('coronadata.dt')
            c = conn.cursor()
            c.execute("""INSERT INTO stats VALUES(?,?,?,?,?,?,?)""" ,
            (dtime.strftime("%x"),new_cases,new_deaths, active_cases,total_corona_cases,total_cured,total_deaths))
            conn.commit()
            conn.close()
    #print(type(data_list[0][1]))
    #print(dtime.strftime("%x"))
    #print(type(dtime.strftime("%x")))        
    #print(data_list[0][1]==dtime.strftime("%x"))
    return new_cases, new_deaths, active_cases, total_corona_cases, total_cured, total_deaths

new_cases, new_deaths, active_cases, total_corona_cases, total_cured, total_deaths = corona_statistics()



#second function for printing
def print_data():
    from datetime import datetime
    dtime =datetime.now()



    print()
    print(f"* მთლიანობაში დაღუპულია {total_deaths:,} ადამიანი {total_corona_cases:,} შემთხვევიდან. \nსიკვდილიანობის პროცენტული მაჩვენებელი არის {total_deaths / total_corona_cases :.2%}.")
    print()
    print(f"* გამოჯანმრთელებულია {total_cured:,} ადამიანი რაც არის {total_cured/ (total_corona_cases) :.2%}." )
    print()
    print(f"* ამჟამად მკურნალობას გადის {active_cases:,} დაავადებულების {active_cases/ total_corona_cases:.2%}.")
    print()
    print(f"* დღევანდელი მონაცემებით გვაქვს დაინფიცირების {new_cases}")# შემთხვევა რაც არის {new_cases/highest_daily_case :.2%}\nმაქსიმალური დაინფიცირების მაჩვენებლისა რომელიც იყო {highest_daily_case}, გასული წლის 5 დეკემბერს.")
    print()
    #print(f"* დღევანდელი გამოჯანმრთელებულთა რიცხვი უდრის {new_curred}.")
    #print()
    print(f"* დღევანდელი რიცხვი სიკვდილიანობისა არის {new_deaths}.") #\nრაც მაქსიმალური დღიური სიკვდილიანობის მაჩვენებლის {new_death/highest_daily_death :.2%} არის. \nმაქსიმალური იყო {highest_daily_death}.")
    print()
    print("* როგორც ამ მონაცემებიდან ვხედავთ საკმაოდ პოზიტიურად მივდივართ.")# ბოლო 1 თვეა, რიცხვები იკლებს.

print_data()  
print()
#print("after change")
print()
conn = sqlite3.connect('coronadata.dt')
c = conn.cursor()
#c.execute("DELETE  FROM stats WHERE rowid > '7'")
c.execute("SELECT rowid, * FROM stats")
mylist = c.fetchall()
for item in mylist:
    print(item)  

conn.commit()
conn.close()



#if __name__=="__main__":
#    corona_statistics()
#    print_data()

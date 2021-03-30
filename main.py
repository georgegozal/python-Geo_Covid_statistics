# -*- coding: utf-8 -*-
import sqlite3

def corona_statistics():
    import requests 
    from bs4 import BeautifulSoup as BS
    #import date and time module
    from datetime import datetime
    dtime =datetime.now()

    # start parsing 
    result = requests.get("https://www.worldometers.info/coronavirus/country/georgia/")
    soup = BS(result.text, "lxml")
    ge_result = requests.get('https://stopcov.ge/ka/')
    wsoup = BS(ge_result.text, features='lxml')

    # colect data
    new_cases= int(soup.select(".news_li strong")[0].getText().split()[0])
    new_deaths= int(soup.select(".news_li strong")[1].getText().split()[0])
    total_deaths = int(soup.select(".maincounter-number span")[1].getText().replace(",","").replace(" ",""))
    total_corona_cases=int(soup.select(".maincounter-number  span")[0].getText().replace(",","").replace(" ",""))
    total_cured = int(soup.select(".maincounter-number span")[2].getText().replace(",","").replace(" ",""))
    active_cases = total_corona_cases - total_cured - total_deaths

    antigen_test = int( wsoup.select('.statistic-square')[1].select('.quantity-numver')[1].text)
    pcr_test = int(wsoup.select('.statistic-square')[1].select('.quantity-numver')[2].text)
    
    conn = sqlite3.connect('coronadata.dt')
    c = conn.cursor()
    # create query
    c.execute("SELECT rowid, date FROM stats ORDER BY 1 DESC LIMIT 1")
    #export list column date`s data
    date_r = c.fetchall()
    conn.close()
    # change database data 
    # if current time  > 9:00 continue 
    if int(dtime.strftime("%H")) >= 9:
        #if our data from database is not the same as todays date then continue 
        if date_r[0][1]!=dtime.strftime("%x"):
            conn = sqlite3.connect('coronadata.dt')
            c = conn.cursor()
            #insert values in the database 
            c.execute("""INSERT INTO stats VALUES(?,?,?,?,?,?,?,?,?)""" ,
            (dtime.strftime("%x"),new_cases,new_deaths, active_cases,total_corona_cases,total_cured,total_deaths,antigen_test,pcr_test))
            conn.commit()
            conn.close()       
    return new_cases, new_deaths, active_cases, total_corona_cases, total_cured, total_deaths, antigen_test, pcr_test

new_cases, new_deaths, active_cases, total_corona_cases, total_cured, total_deaths, antigen_test, pcr_test = corona_statistics()



#second function for printing
def print_data():
    # again import datetime for printing date
    from datetime import datetime
    dtime =datetime.now()
    #import more data from database
    conn = sqlite3.connect('coronadata.dt')
    c = conn.cursor()
    c.execute("SELECT MAX(new_cases), date FROM stats")
    max_nc=c.fetchall()
    c.execute("SELECT MAX(new_deaths), date FROM stats")
    max_dths=c.fetchall()
    conn.close()

    print("\n", dtime.strftime("%d %B %Y ამ დროის მონაცემებით შედეგები ასეთია: \n"))
    print(f"* მთლიანობაში დაღუპულია {total_deaths:,} ადამიანი {total_corona_cases:,} შემთხვევიდან. \nსიკვდილიანობის პროცენტული მაჩვენებელი არის {total_deaths / total_corona_cases :.2%}. \n")
    print(f"* გამოჯანმრთელებულია {total_cured:,} ადამიანი რაც არის {total_cured/ (total_corona_cases) :.2%}.\n" )
    print(f"* ამჟამად მკურნალობას გადის {active_cases:,} დაავადებულების {active_cases/ total_corona_cases:.2%}.\n")
    print(f"* დღევანდელი მონაცემებით გვაქვს დაინფიცირების {new_cases} შემთხვევა რაც არის {new_cases/int(max_nc[0][0]) :.2%}\nმაქსიმალური დაინფიცირების მაჩვენებლისა რომელიც იყო {max_nc[0][0]}, {max_nc[0][1]} . \n")
    print(f'* დღევანდელი მონაცემებით დატესტილია სულ {antigen_test+pcr_test}, \n {antigen_test} იყო ანტიგენის ტესტი {pcr_test} PCR ტესტი.\n დაინფიცირების მაჩვენებელი არის {new_cases / (antigen_test+pcr_test):.2%}. \n')
    print(f"* დღევანდელი რიცხვი სიკვდილიანობისა არის {new_deaths}.\n რაც მაქსიმალური დღიური სიკვდილიანობის მაჩვენებლის {new_deaths/int(max_dths[0][0]) :.2%} არის. \nმაქსიმალური იყო {max_dths[0][0]}, {max_dths[0][1]}. \n")
    print('* აცრა დაიწყო 15 მარტს ასტრა ზენეკას ვაქცინით. \n')
    #print("* როგორც ამ მონაცემებიდან ვხედავთ საკმაოდ პოზიტიურად მივდივართ.")# ბოლო 1 თვეა, რიცხვები იკლებს.
    


def dataframe():
    import pandas as pd
    from pandas import DataFrame
    conn = sqlite3.connect("coronadata.dt")
    sql_query = ''' SELECT rowid,* FROM stats; '''


    my_data_frame =pd.read_sql_query(sql_query, conn, index_col='rowid', parse_dates='date')                        
    #my_data_frame = DataFrame(pd.read_sql(sql_query, conn)).set_index('rowid')
    my_data_frame.columns=[ 'Date', 'New cases', 'New deaths', 'Active cases', 'Total Corona cases','Got recovered','Total deaths', 'Antigen test', 'PCR test']
    
    #print("\n",my_data_frame)
    print("\n",my_data_frame.tail(15))
    #print("\n", my_data_frame.describe()) # describe 
    #print(my_data_frame.info())
if __name__=="__main__":
    corona_statistics()
    dataframe()
    print_data()

# -*- coding: utf-8 -*-
import sqlite3
import pandas as pd
from datetime import datetime
dtime =datetime.now()

def corona_statistics():
    import requests 
    from bs4 import BeautifulSoup as BS
    # start parsing 
    result = requests.get("https://www.worldometers.info/coronavirus/country/georgia/")
    soup = BS(result.text, "lxml")
    ge_result = requests.get('https://stopcov.ge/ka/')
    wsoup = BS(ge_result.text, features='lxml')

    # colect data
    new_cases= int(soup.select(".news_li strong")[0].getText().split()[0].replace(",",""))
    new_deaths= int(soup.select(".news_li strong")[1].getText().split()[0])
    total_deaths = int(soup.select(".maincounter-number span")[1].getText().replace(",","").replace(" ",""))
    total_corona_cases=int(soup.select(".maincounter-number  span")[0].getText().replace(",","").replace(" ",""))
    total_cured = int(soup.select(".maincounter-number span")[2].getText().replace(",","").replace(" ",""))
    active_cases = total_corona_cases - total_cured - total_deaths

    antigen_test = int( wsoup.select('.statistic-square')[1].select('.quantity-numver')[1].text)
    pcr_test = int(wsoup.select('.statistic-square')[1].select('.quantity-numver')[2].text)
    percent = round(new_cases / (antigen_test+pcr_test) *100 ,2)
    conn = sqlite3.connect('coronadata.dt')
    c = conn.cursor()
    #insert values in the database 
    c.execute("""INSERT INTO stats VALUES(?,?,?,?,?,?,?,?,?,?)""" ,
        (dtime.strftime("%x"),new_cases,new_deaths, active_cases,total_corona_cases,total_cured,total_deaths,antigen_test,pcr_test,percent))
    conn.commit()
    conn.close()       


# check time and last row to run function 
if int(dtime.strftime("%H")) >= 9:
    conn = sqlite3.connect('coronadata.dt')
    c = conn.cursor()
    c.execute("SELECT rowid, date FROM stats ORDER BY 1 DESC LIMIT 1")
    date = c.fetchone()[1]
    conn.close() 
    if date !=dtime.strftime("%x"):
        corona_statistics()


def dataframe():

    conn = sqlite3.connect("coronadata.dt")
    sql_query = ''' SELECT rowid,* FROM stats; '''


    mdf =pd.read_sql_query(sql_query, conn, index_col='rowid', parse_dates='date') 
    mdf.columns=[ 'Date', 'New cases', 'New deaths', 'Active cases', 'Total Corona cases', 'Got recovered', 'Total deaths', 'Antigen test', 'PCR test', 'positive %']

    print("\n",mdf.tail(9))
    #print("\n", mdf.describe()) # describe 
    ncases=mdf[mdf['New cases']==mdf['New cases'].max()]
    ndeaths=mdf[mdf['New deaths']==mdf['New deaths'].max()]
    print("\n", dtime.strftime("%d %B %Y ამ დროის მონაცემებით შედეგები ასეთია: \n"))
    print(f"* მთლიანობაში დაღუპულია {mdf['Total deaths'].values[-1]:,} ადამიანი {mdf['Total Corona cases'].values[-1]:,} შემთხვევიდან. სიკვდილიანობის პროცენტული მაჩვენებელი არის {mdf['Total deaths'].values[-1] / mdf['Total Corona cases'].values[-1] :.2%}. \n")
    print(f"* გამოჯანმრთელებულია {mdf['Got recovered'].values[-1]:,} ადამიანი რაც არის {mdf['Got recovered'].values[-1] / mdf['Total Corona cases'].values[-1] :.2%}. \n" )
    print(f"* ამჟამად მკურნალობას გადის {mdf['Active cases'].values[-1]:,} დაავადებულების {mdf['Active cases'].values[-1] / mdf['Total Corona cases'].values[-1]:.2%}.\n")
    print(f"* დღევანდელი მონაცემებით გვაქვს დაინფიცირების {mdf['New cases'].values[-1]} შემთხვევა რაც არის {mdf['New cases'].values[-1] / ncases['New cases'].values[-1] :.2%}\nმაქსიმალური დაინფიცირების მაჩვენებლისა რომელიც იყო {ncases['New cases'].values[-1]}, {str(ncases['Date'].values[-1]).split('T')[0]}-ს . \n")
    print(f"* დღევანდელი მონაცემებით დატესტილია სულ {mdf['Antigen test'].values[-1] + mdf['PCR test'].values[-1]}: {mdf['Antigen test'].values[-1]} იყო ანტიგენის ტესტი {mdf['PCR test'].values[-1]} PCR ტესტი. დაინფიცირების მაჩვენებელი არის {mdf['positive %'].values[-1]}%. \n")
    print(f"* დღევანდელი რიცხვი სიკვდილიანობისა არის {mdf['New deaths'].values[-1]}. რაც მაქსიმალური დღიური სიკვდილიანობის მაჩვენებლის {mdf['New deaths'].values[-1] / ndeaths['New deaths'].values[-1] :.2%} არის. \nმაქსიმალური იყო {ndeaths['New deaths'].values[-1]}, {str(ndeaths['Date'].values[-1]).split('T')[0]}-ს. \n")
    #print('* აცრა დაიწყო 15 მარტს ასტრა ზენეკას ვაქცინით. \n')
    #print("* როგორც ამ მონაცემებიდან ვხედავთ საკმაოდ პოზიტიურად მივდივართ.")# ბოლო 1 თვეა, რიცხვები იკლებს.

    
if __name__=="__main__":
    dataframe()
    

import requests 
from bs4 import BeautifulSoup as BS
import pandas as pd
from pandas import DataFrame
import sqlite3

result = requests.get('https://www.worldometers.info/coronavirus/#countries')
soup = BS(result.text, "lxml")

countries = []
for i in soup.select('.mt_a'):
    countries.append(i.text.lower().replace(" ","-"))

def corona_statistics(countries):
    from datetime import datetime
    dtime =datetime.now()
        
    conn = sqlite3.connect('alldata.dt')
    c = conn.cursor()
    # create query
    c.execute("SELECT rowid, date FROM stats ORDER BY 1 DESC LIMIT 1")
    #export list column date`s data
    date_r = c.fetchall()
    conn.close()
        
    if int(dtime.strftime("%H")) >= 9:
        #if our data from database is not the same as todays date then continue
        if date_r[0][1]!=dtime.strftime("%x"):
            
            for country in countries:
                result=requests.get(f'https://www.worldometers.info/coronavirus/country/{country}/')
                soup = BS(result.text, "lxml")
                
                # collect data
                try:
                    new_cases = int(soup.select(".news_li strong")[0].getText().split()[0].replace(",",""))
                except:
                    new_cases = 0            
                try:    
                    new_deaths= int(soup.select(".news_li strong")[1].getText().split()[0])
                except:
                    new_deaths = 0
                try:    
                    total_deaths = int(soup.select(".maincounter-number span")[1].getText().replace(",","").replace(" ",""))
                except:
                    total_deaths = 0
                try:
                    total_corona_cases=int(soup.select(".maincounter-number  span")[0].getText().replace(",","").replace(" ",""))
                except:
                    total_corona_cases =0
                try:    
                    got_recovered = int(soup.select(".maincounter-number span")[2].getText().replace(",","").replace(" ",""))
                except:
                    got_recovered=0
                active_cases = total_corona_cases - got_recovered - total_deaths
                conn = sqlite3.connect('alldata.dt')
                c = conn.cursor()
                #insert values in the database 
                c.execute("""INSERT INTO stats VALUES(?,?,?,?,?,?,?,?)""" ,
                (dtime.strftime("%x"),country,new_cases,new_deaths, active_cases,total_corona_cases,got_recovered,total_deaths))
                conn.commit()
                conn.close()
            
            
corona_statistics(countries)


conn = sqlite3.connect("alldata.dt")
sql_query = ''' SELECT rowid,* FROM stats; '''

mdf =pd.read_sql_query(sql_query, conn, index_col='rowid', parse_dates='date') 
mdf.columns=[ 'Date,','Country', 'New cases,', 'New deaths,', 'Active cases,', 'Total Corona cases,', 'Got recovered,', 'Total deaths,']

#print(mdf.dtypes)
#print("\n",mdf['New deaths,'].value_counts())
print("\n",mdf.tail(9))
#print("\n", mdf.describe()) # describe 
#print('\n', mdf.info())

    
if __name__=="__main__":
    corona_statistics(countries)
    #dataframe()


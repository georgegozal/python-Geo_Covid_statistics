
import requests 
from bs4 import BeautifulSoup as BS
#import sqlite3

from datetime import datetime
dtime =datetime.now()

result = requests.get("https://www.worldometers.info/coronavirus/country/georgia/")

soup = BS(result.text, "lxml")

def corona_statistics():
    corona_cases=int(soup.select(".maincounter-number  span")[0].getText().replace(",","").replace(" ",""))
    got_cured = int(soup.select(".maincounter-number span")[2].getText().replace(",","").replace(" ",""))
    death = int(soup.select(".maincounter-number span")[1].getText().replace(",","").replace(" ",""))
    active_cases = corona_cases - got_cured - death
    new_cases= int(soup.select(".news_li strong")[0].getText().split()[0])
    #new_curred = 1080
    new_death= int(soup.select(".news_li strong")[1].getText().split()[0])
    highest_daily_case = 5450
    highest_daily_death = 53
    
    print(f"* მთლიანობაში დაღუპულია {death:,} ადამიანი {corona_cases:,} შემთხვევიდან. \nსიკვდილიანობის პროცენტული მაჩვენებელი არის {death / corona_cases :.2%}.")
    print()
    print(f"* გამოჯანმრთელებულია {got_cured:,} ადამიანი რაც არის {got_cured/ (corona_cases) :.2%}." )
    print()
    print(f"* ამჟამად მკურნალობას გადის {active_cases+new_cases:,} დაავადებულების {active_cases/ (corona_cases +new_cases):.2%}.")
    print()
    print(f"* დღევანდელი მონაცემებით გვაქვს დაინფიცირების {new_cases} შემთხვევა რაც არის {new_cases/highest_daily_case :.2%}\nმაქსიმალური დაინფიცირების მაჩვენებლისა რომელიც იყო {highest_daily_case}, გასული წლის 5 დეკემბერს.")
    print()
    #print(f"* გამოჯანმრთელებულთა რიცხვი უდრის {new_curred}.")
    #print()
    print(f"* დღევანდელი რიცხვი სიკვდილიანობისა არის {new_death}.") #\nრაც მაქსიმალური დღიური სიკვდილიანობის მაჩვენებლის {new_death/highest_daily_death :.2%} არის. \nმაქსიმალური იყო გასული წლის 19 დეკემბერს: 53 ადამიანი.")
    print()
    print("* როგორც ამ მონაცემებიდან ვხედავთ საკმაოდ პოზიტიურად მივდივართ ბოლო 1 თვეა, რიცხვები იკლებს.")
    return " "
    
corona_statistics()

# Database connecting 
#conn = sqlite3.connect('corona_data.dt')
# Create cursor
#c = conn.cursor()

"""c.execute('''CREATE TABLE stats(
id INTEGER PRIMARY KEY,
date TEXT, 
new_cases INTEGER, 
new_deaths INTEGER, 
got_cured INTEGER, 
total_corona_cases INTEGER,
total_cured INTEGER,
total_deaths INTEGER)
''');
"""

# commi our comand 
#conn.commit()

# close our connection 
#conn.close()


#if __name__=="__main__":

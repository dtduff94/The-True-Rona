import requests
import mysql.connector
from datetime import date, timedelta
from bs4 import BeautifulSoup

#SQL connection data to connect and save the data in
HOST = "localhost"
USERNAME = "scraping_sample_user1"
PASSWORD = "Bullseye18!"
DATABASE = "corona"

db = mysql.connector.connect(
    host = "localhost",
    user = "scraping_sample_user1",
    password = "Bullseye18!",
    database = "corona"
)

mycursor = db.cursor()

# List of US states:
states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virgina", "Washington", "West Virginia", "Wisconsin", "Wyoming", "Guam", "Northern Mariana Islands", "Puerto Rico", "United States Virgin Islands", "USA Total"]

#Create Table
for state in states:
    try:
        # SQL statement
        sql = "CREATE TABLE IF NOT EXISTS `" + state + "` (date DATE PRIMARY KEY, total_cases INT(10), new_cases INT(10), total_deaths INT(10), new_deaths INT(10), active_cases INT(10), tot_cases_1m_pop INT(10), deaths_1m_pop INT(10), total_tests INT(10), tests_1m_pop INT(10));"

        # Execute SQL statement
        mycursor.execute(sql)

        # Commit SQL statement
        db.commit()

    except:
        # Rollback if error
        db.rollback()
        pass
    
#URL to be scraped
url_to_scrape = 'https://www.worldometers.info/coronavirus/country/us/'

#Load html's plain data into a variable
plain_html_text = requests.get(url_to_scrape)

#parse the data
soup = BeautifulSoup(plain_html_text.text, "html.parser")

#Get the name of the class
name_of_class = soup.h3.text.strip()

#Get all data associated with this class
us_table = soup.find("table", {"id": "usa_table_countries_yesterday"});

for row in us_table.select("tr"):         #Iterate through the rows inside the table
    cells = row.findAll("td")             #Get all cells inside the row
    if(len(cells) > 0):                   #check if there is at least one td cell inside this row
        #get all the different data from the table's tds
        usa_state = (cells[0].text.strip()).replace(",", "")
        total_cases = (cells[1].text.strip()).replace(",", "")
        new_cases = ((cells[2].text.strip()).replace(",", ""))[1:]
        total_deaths = (cells[3].text.strip()).replace(",", "")
        new_deaths = ((cells[4].text.strip()).replace(",", ""))[1:]
        active_cases = (cells[5].text.strip()).replace(",", "")
        tot_cases_1m_pop = (cells[6].text.strip()).replace(",", "")
        deaths_1m_pop = (cells[7].text.strip()).replace(",", "")
        total_tests = (cells[8].text.strip()).replace(",", "")
        tests_1m_pop = (cells[9].text.strip()).replace(",", "")

        # Set null values to 0 so SQL database accepts them
        if not total_cases:
            total_cases = 0
        if not new_cases:
            new_cases = 0
        if not total_deaths:
            total_deaths = 0
        if not new_deaths:
            new_deaths = 0
        if not active_cases:
            active_cases = 0
        if not tot_cases_1m_pop:
            tot_cases_1m_pop = 0
        if not deaths_1m_pop:
            deaths_1m_pop = 0
        if not total_tests:
            total_tests = 0
        if not tests_1m_pop:
            tests_1m_pop = 0
        
        for state in states:
            try:
                sql_two = "INSERT INTO `" + usa_state + "`(date, total_cases, new_cases, total_deaths, new_deaths, active_cases, tot_cases_1m_pop, deaths_1m_pop, total_tests, tests_1m_pop) VALUES('" + str(date.today() - timedelta(days = 1)) + "', '" + str(total_cases) + "', " + str(new_cases) + ", " + str(total_deaths) + ", " + str(new_deaths) + ", " + str(active_cases) + ", " + str(tot_cases_1m_pop) + ", " + str(deaths_1m_pop) + ", " + str(total_tests) + ", " + str(tests_1m_pop) + ");"

                # Execute SQL statement
                mycursor.execute(sql_two)

                # Commit SQL statement
                db.commit()

            except:
                db.rollback()
                pass

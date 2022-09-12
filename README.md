## TASK

The purpose of this application is to collect, parse and save requested data
from the certain website. Test task stored in "Test Task.pdf" file.


## DESCRIPTION

This is the CLI app designed for collecting data with synchronous (using 
Selenium) or asynchronous (using aiohttp and asyncio) operation scheme, parse
it (using BeautifulSoup) and save it to PostgreSQL or Google Sheets 
spreadsheet. 
The "python app.py" command can be used to start the application. With this 
command will start parsing pages from the first to the tenth with 
sync scenario using Selenium and saving parsed data to the PostgreSQL DB 
by default. For changing parameters CLI command can be used.
There are four parameter for command: 

 - page_from : int -> Specified the site page to start parsing.
 - page_to : int -> Specified the site page to end parsing.
 - save_to : str -> Specified how the data will be saved (choices are "postgres" 
   or "google_sheets").
 - parser_type : str -> Specified which type of parsing to use (choices are "sync"
   or "async").
   
So, for example: command "python app.py 10 100 google_sheets async" will start
app to parse pages from 10 to 100 with async scenario and save parsed data to
Google Sheets spreadsheet.


## PREPARATION

 - Please clone repository to local machine 
 - As app is dockerized, Docker-Compose container should be built before using. 
   For this purpose use two commands:
   - docker-compose build
   - docker-compose up -d
 - There is "credentials.json" file required. As this file containing security
   info and can't be uploaded to Git, it is necessary to save file 
   "credentials.json" to working directory (/dataox_test_task). This file can 
   be created as per [this guide](https://developers.google.com/workspace/guides/create-credentials#create_credentials_for_a_service_account).
 - This app using some Environment Variables. .env file containing security
   info and in normal case should not be uploaded to the Git. But for testing
   purpose there is .env.example file, containing some default values. So, for 
   normal work of app, please rename .env.example file to .env.
 - App can be started now using 
   "python app.py [page_from] [page_to] [save_to] [parser_type]" command.


## ADDITIONAL

Database dump (both in .csv and .sql format) stored in ./db_dump directory.
Also, there is prepared [Google Sheets spreadsheet](https://docs.google.com/spreadsheets/d/1_MXpz6URmT-Cz5Tas9SlirPQO9tc75fT6u5vXqg26LA/edit#gid=0).
 

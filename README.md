# data-wrangling-with-python-and-sql

A CLI app which use programmatic access to the database sql server.

## Usage

* `git clone https://github.com/bngom/data-wrangling-with-python-and-sql`

* `cd data-wrangling-with-python-and-sql`

* `py -m venv env` Create a virtual environment

* `.\env\Scripts\activate` Activate the virtual environment

* `pip install .` Install the setup for the command line interface 

* `pysql-cli --help` To check the usage of the CLI. Will also install requirements.

* `pysql-cli generate-last-survey-structure` Create a file `lastsurveystructure.csv` in *db* folder 

* `pysql-cli get-last-survey-structure` Get the last known survey structure 

* `pysql-cli get-view-surveydata` Check if the view ***vw_AllSurveyData*** exists 

* `pysql-cli update-survey-structure "YOUR QUERY"` Trigger the view creation (on INSERT, UPDATE or DELETE on SurveyStructure table) 
    - example `pysql-cli update-survey-structure "DELETE FROM SurveyStructure WHERE SurveyId = 2  AND QuestionId = 3"`
    
* `pysql-cli get-view-surveydata` Returns data from ***vw_AllSurveyData***



# AI Agent Framework

A modular AI-powered data engineering framework built in Python.

## Features

- Modular AI agents
- Data collection
- Data cleaning
- Data validation
- Automated reporting
- Dashboard automation
- Multi-source connectors
- FastAPI backend
- Scheduling
- AI orchestration

## Project Structure

(We'll fill this in as the framework grows.)

## Installation

```bash
pip install -r requirements.txt
```

## Status

🚧 In Development

##  git hub updates
- git status
- git add <File>
- git status - checks if the files are ready for commitment
- git commit -m "Project name i.e Initial AI Agent Framework structure" - local
- git branch - checks your branch
- git add . - saves everything at once
- git push origin main OR git push- lets you save everything on the main repository on the account

## Accessing Excel files
- pip install openpyxl

## Architecture

                 Data Sources
                      |
        --------------------------------
        |                              |
      CSV                          Excel
        |                              |
        ↓                              ↓
   CSVConnector              ExcelConnector
              \              /
               \            /
                Connector Registry
                       |
                       ↓
                Collection Agent
                       |
                       ↓
                Cleaning Agent
                       |
                       ↓
              Validation Agent
                       |
                       ↓
             Reporting Agent


## Testing

Run:

python test_registry.py

Tests:
- Connector registration
- CSV connector loading
- Excel connector loading

Run:

python test_collection_agent.py

Tests:
- Collection Agent workflow
- Connector selection
- Data collection metrics


## Supported Connectors

| Source | Connector | Status |
|---|---|---|
| CSV | CSVConnector | ✅ Complete |
| Excel | ExcelConnector | ✅ Complete |
| REST API | RESTAPIConnector | Planned |
| SQL Database | SQLConnector | Planned |



# Refactor connector registration into setup module
Agents → do work
Registry → routes connectors
Connector setup → configures available data sources
Connectors → handle data access


                         User / Pipeline
                              |
                              ↓
                   +----------------------+
                   |   Collection Agent   |
                   +----------------------+
                              |
                              ↓
                   +----------------------+
                   | Connector Setup      |
                   | (configuration)      |
                   +----------------------+
                              |
                              ↓
                   +----------------------+
                   | Connector Registry   |
                   | (routing logic)      |
                   +----------------------+
                              |
              --------------------------------
              |                              |
              ↓                              ↓
      +---------------+              +---------------+
      | CSV Connector |              | Excel Connector|
      +---------------+              +---------------+
              |                              |
              --------------------------------
                              |
                              ↓
                         DataFrame

## Rest API Connector
- lets the collection access data from APIs e.g Openweather
- Update registry file so it detects connectors using .file (.csv,etc) and URL extentions
- pip install python-dotenv - lets you run an API key from your .env
- .gitignore prevents API key being shared to the public on github
- Make sure your pip install is installed in the root python file, so the API recall works

                 Data Source
                      |
      ---------------------------------
      |               |               |
      ↓               ↓               ↓
   CSV File      Excel File      REST API
      |               |               |
      ↓               ↓               ↓
 CSVConnector   ExcelConnector   RESTAPIConnector
         \          |          /
          \         |         /
           +-----------------+
           | ConnectorRegistry|
           +-----------------+
                    |
                    ↓
            CollectionAgent
                    |
                    ↓
             pandas DataFrame



 ## SAVE YOUR FILE ON GITHUB            
Save process: git add .
git commit -m "Add REST API connector for live weather data"
git push
##



## 🏗️ SQL lite connector set up - useful for SQL queries.

1. Create a sample database (.db).
2. Update the sqlite connector - connect();collect();close().
3. Connect the connector_set up file with the new sqlite connector.
4. Created a sample database and ran it in the terminal: python create_sample_database.py
      - Create the .py file in the root, so the new sql lite file is created in the data folder.
5. Added a query parameter in the collect function () so users can query data bases from the collection agent. Logic remains the same for other data files.
6. Save the updates on github: 
     git add .
     git commit -m "Add SQL query support to SQLite connector"
     git push
7. Structure:
                         Collection Agent
                           |
                           | source + optional query
                           ↓
                  Connector Registry
                           |
       ┌──────────┬───────┼──────────┐
       ↓          ↓       ↓          ↓
      CSV       Excel   REST API    SQLite
       |          |       |           |
       ↓          ↓       ↓           ↓
   collect()  collect() collect()  collect(query)
                                      |
                                      ↓
                                  SQL Database
                                      |
                                      ↓
                                  DataFrame

                                  

## sharepoint Connector set up - Useful for private enterprise databases.

1. 



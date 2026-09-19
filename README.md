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
- pip install python-dotenv - lets you run an API key from your .env.
- pn python file,load_dotenv() *  # Load environment variables 
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

                                  

##   Sharepoint Connector set up - Useful for private enterprise databases.

                    SharePoint Development

                         App Registration
                                ↓
                         Authentication
                                ↓
                         Graph API Test
                                ↓
                      SharePoint File Access
                                ↓
                       SharePointConnector
                                ↓
                       Connector Registry
                                ↓
                       Collection Agent
## Steps:

     1. Install Microsoft libraries :
          - Installing the libraries is essensial for creating our Graph API.
          - python -m pip install msal requests ( Install pip in roots)
          - add to the requirements file: msal 
                                           requests

     2. Create a Microsoft Entra app registration:


      - Deliverables:
                    Tenant ID (Choose Microsoft organisation: Microsoft Entra code)
                    Client ID (choose application: application code i.e virtual ID )
                    Client Secret (credentials to log into application)

          - This relates to the Graph API test - we need to create an application ID so our python system communitcates with Microsft Graph, which then talks to Microsoft services.
          - The Mircosoft entra acts as a digital security gurad and directory for apps and devices. The admin center gives admins the abiity overlook multiple produtcs Microsoft entra has to offer i.e authentification, governance, verify credentials, ID protection, etc.
          - To gain full access to Microsoft Entra, you need to either sign up for Microsoft Azure ( acts as a cluster of large computer, server, or cloud storage great for scaling) of join Microsoft 365 dev program.
          - Microsoft 365 dev program: I picked Mircosoft Graph, Copilot, and sharepoint frame work.
          ( No more developer access - Microsoft restricted it)
          - Sign up for for free Azure.
          - Entra is the lock, client secret is the key, Graph retrives data from sharepoint.

          - Create an app through registration - choose single tenant only to give only ureself access to the sharepoint files ( multi entra is for selling apps in scale).
          - leave redirect URL blank - client secret and app registration is used to make the app.
          - go to certificates and secret on the app - add client secrets.
          - Add Microsoft graph permissions: 
               - select API permissions and add a permission.
               - pick the Mircosoft Graph option, and choose application permissions(app runs in the background).
               - Type Files -> click the dropdown -> check Files.Read.All (or Files.ReadWrite.All if your script needs to upload or modify files).
               - Type Sites -> click the dropdown -> check Sites.Read.All.
               - click - Grant admin consent for all default directory.
          The App created runs like a virtual ID - it lets us access data in sharepoint or any app supported by Microsoft Azure.
           Process:
               1. log into sharepoint - log in with ure admin account.
               2. search apps for sharepoint.
               3. open library on left hand side and click documents.
               4. drag and drop files.
          * Sharepoint only exists in a business acount, so get free trail business account to help with this.
          *get a business 365 business account - gives access to lots of apps including sharepoint, and connects it to you Entra and Azure accounts.
          - Created 2 Microsoft entra accounts and linked one of them to the Microsoft business account so you can access sharepoint.
          - Use the email: name@ your-domain-name.onmicrosoft.com to log into the entra and 365.
          - While sharepoint is loading, go to domain-name.sharepoint.com to add documents in your folder.

## Freelance
  - Scenario A: They give you the keys (The "Single-Tenant" Custom Way)
  If you build a custom script or a tool tailored for one specific company, they will handle the setup inside their own system.
  Their Admin will log into their own Microsoft Entra portal.
  They will create the App Registration, generate a Client Secret, and grant the SharePoint permissions.
  They will hand you three pieces of text: Their Tenant ID, Their Client ID, and Their Client Secret.
  Your Action: You plug those three variables into your collection agent, and it connects directly to their data pipeline. 
  You never have to log into their Microsoft 365 dashboard or know their admin password.

         - Once the Graph Id worsk, find your sharepoint site ID: https://yourcompany.sharepoint.com/sites/Analytics (use the URL)
         - we need to locate the site ID ( URL), drive ID/libraries ( where it's stored ): _drives.py, ID the folders: _files.py, list the files inside the folder: _folder.py.
         - last step is to test the retrieval use he drive ID, list of files ID to pull the data.
         - You need to know the site URL and optionally the drive name to retrieve the data



#####   🧹  CLEANING AGENT:
          Source
          ↓
          CollectionAgent
          ↓
          DataFrame
          ↓
          CleaningAgent
          ↓
          Clean DataFrame

 ## Cleaning duties:
     1. Missing values
          - Identify nulls
     2. Decide whether to remove, fill, or preserve them
          - Duplicate records
          - Detect duplicates
          - Remove duplicates when appropriate
     3. Column names
          - Standardize column names
          - Remove unnecessary whitespace
          - Normalize capitalization
     4. Data types
          - Detect incorrect types
          - Convert dates, numbers, strings, etc.
     5. Whitespace / text cleanup
          - " John " → "John"
          - Normalize empty strings
     6. Basic data validation
          - Identify suspicious values
          - Flag problems rather than blindly changing data
     7. Cleaning metrics
          - Number of rows before/after
          - Number of duplicates removed
          - Missing values detected
          - Columns modified
          - Data types changed

- Break the cleaning agent into 2 stages:
     - Prolife the data.
     - clean the data.

- Created a utility for the data cleaner - this will determine what kind of cleaning is needed.
- similar to our connector_setup and registry, this file will determine what kind of cleaning activity is needed.

               DataCleaner → performs deterministic cleaning operations.
               CleaningAgent → manages the cleaning process and records what happened.
               Validation agent → Inspect the cleaned DataFrame and determine whether it meets basic quality requirements.
               CollectionAgent → only retrieves data.
- Create validation agent:
Important questions to ask.
 -> Is the DataFrame empty?
 -> Are required columns present?
 -> Are there remaining missing values?
 -> Are there duplicate rows?
 -> Are specified columns numeric?
 -> What is the overall validation status?
  - read-only quality-control stage


## Build the pipeline for all agents - collection, cleaning, and validation agent




## Storage /Persistence layer
 - we need a location to store our validated data.
 Process:
     1. Create a .PY file under the storage folder.
     2. Create a check in the pipeline.py file that ensures the storage feature works.


## Header detector 
- we need to able to detect the correct header in our code before the cleaning and validating agents.
- We should create a header_detector.py file in the utils and apply it to the cleaning agent.
- Our detectors already assume the 1st row is the begining of the dataset, but sometimes the data is incorrect.
- This process will allow our connectors know the begining of the header, before passing along to the cleaning agent and validation agent.

 Process:
 After creating the header detection file and applying them to the connectors, we then input the apply header file to the cleaning agent.
 - In order for the connectors to not read the read the 1st header and true, we input : header=None on each connector.
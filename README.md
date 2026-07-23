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
- git push origin main - lets you save everything on the main repository on the account

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
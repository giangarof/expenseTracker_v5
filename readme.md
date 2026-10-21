# Expense tracker V5

## Branch: main

- This branch uses sqlite

## About

- Fifth version of my Expense Tracker series.
- Continuation of V3, which introduced SQL for database management.
- V5 implements authentication and user verification.
- Expenses are now associated with users through a relationship between the Expense and User models.

# Steps

- Clone the project
- Create a virtual environment: `python3 -m venv <name>`
- Activate the environment: `source <name>/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- To run: `fastapi run main.py --reload`

## To run sqlite

- In the root, type: `sqlite3 <filename_name>.db`

# Previous versions

- [v4](https://github.com/giangarof/expenseTrackerFastAPI_nosql): This version implements FastAPI along with NoSQL (MongoDB)
- [v3](https://github.com/giangarof/expenseTrackerFastAPI_sql): This version implements FastAPI along with SQL (SQLAlchemy)
- [v2](https://github.com/giangarof/expenseTrackerFastAPI): This version implements FastAPI
- [V1](https://github.com/giangarof/expenseTrackerTerminalPython): This version implements vanilla python. Can be used through the terminal.

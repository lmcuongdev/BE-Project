# BE-Project

## Installation

1. Clone the project:

```
git clone git@github.com:lmcuongdev/BE-Project.git
cd ./BE-Project
```

2. Set up virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

3. Install project dependencies:

```
pip install -r requirements.txt
```

4. Use MySQL shell to run the database setup

```
>mysql create database db;
>mysql use db;
>mysql source database.sql;
```

5. Create and update the the correct configuration to the .env file

```
cp .env.example .env
```

## Starting the application

To start running an instance of the server on local machine

```
flask run --port 8888
```

## Testing

First create a new database for testing, then run the database setup again

```
>mysql create database test_db;
>mysql use test_db;
>mysql source database.sql;
```

Configure the .env file, and run the tests

```
pytest --cov --cov-config=.coveragerc --cov-report html
```

The test coverage files can be found in htmlcov folder
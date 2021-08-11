# BE-Project

## Installation

1. Clone the project:
```
git clone git@github.com:lmcuongdev/BE-Project.git
cd ./BE-Project
```
2. Set up Virtualenv:
```
pip install virtualenv
virtualenv venv
source ~/venv/bin/activate
```
3. Install project dependencies:
```
pip install -r requirements.txt
```
4. Use MySQL shell to run the database setup
```
>mysql create database final_project;
>mysql use final_project;
>mysql source database.sql;
```
5. Create and update the the correct configuration to the .env file
```
cp .env.example .env
```

## Starting the application
To start running an instance of the server on local machine
```
python main.py

# DBMS_labwork
This repository contains one single python project to perform laboratory experiments of DBMS subject on your own postgreSQL database, you can add your own experiments by simply giving normal SQL queries as input and it'll perform it and print the results for you

# How to setup environment 

Ensure that python is properly installed in your system 
if not you can search online how to do that...

I'm writing steps for Debian based Linux distro(s) here

## step 1 :- 
first ensure your system is upto date
run:- 
```bash
apt-get update -y && apt-get upgrade -y
```
deal with user permissions urself (use sudo if required)

## step 2:-
Now let's proceed for installing required packages 
run:-
```bash
apt-get install python3-pip git
```

## step 3:-
Clone into the project 
run:-
```bash
git clone https://github.com/pn-projects/DBMS_labwork
```

## step 4:-
load project directory 
run:- 
```bash
cd DBMS_labwork
```

## step 5:-
install required python packages
run:- 
```bash
pip3 install --no-cache-dir -r requirements.txt
```

## step 6:-
create a `.env` file that contains all the environment variables which will be used for connection purposes 
run:- 
```bash
touch .env
```

now open texteditor of your choice and fill all the environment vars

i personally use nano 

```bash
nano .env
```

fill all the required environment vars 
which you'll find in [sample.env](https://github.com/pn-projects/DBMS_labwork/sample.env)

## step 7:-

now you're ready to go 
you can execute python files located in the project directory as per your convenience 

we currently support 3 types of SQL databases for the operation:- 

- MySQL
- SQLite (python)
- postgreSQL

i recommend SQLite if you are working on local DB 
&
if you have either postgre or MySQL hosted somewhere then you can connect with it and work on it 

you can manipulate vars in [config.py](https://github.com/pn-projects/DBMS_labwork/config.py) as per your convenience and vars required to connect ur db as per the host you are using 

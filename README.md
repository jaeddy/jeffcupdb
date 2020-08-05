# Jefferson Cup DB

This codebase was forked from [**espn-ffb**](https://gitlab.com/raphattack/espn-ffb) by @raphattack. **espn-ffb** is a project to query fantasy football data from ESPN's API and persist it in your own database. There is a very basic web component with a few views built using Flask that allows you to self-host your own fantasy football league page for things such as historical records, weekly recaps, etc.

The Jefferson Cup is a long running fantasy league among UVA alumns and friends. This project builds on and customizes the **espn-ffb** application to provide an interactive interface for exploring current and historical Jeff Cup league data.

*This repo will be evolving dramatically over the next several weeks/months, so any of the documentation below should be approached with caution.*

#### Pre-requisites:

*  [Python](https://www.python.org/download/releases/3.0/)
*  [PostgreSQL](https://www.postgresql.org/download/)
*  uWSGI (optional, but recommended if running in production)


## Requirements:
```
pip install -r requirements.txt
```

## Config:

Edit [config.py](jeffcupdb/config.py) with your own:
*  Enter your database credentials in `envvars-{dev|prod}`.
*  Set the name, host, and port of the database you are using in `envvars-{dev|prod}`
*  `LEAGUE_ID`
*  `swid` (private leagues)
*  `espn_s2` (private leagues)
  
To find your `swid` and `espn_s2` in Chrome, go to **DevTools > Application > Cookies >** https://fantasy.espn.com.

## Setup:
```
source envvars-{dev|prod} && python -m jeffcupdb.initialize
```

## Run:
```
# run with python
python -m jeffcupdb.app

# run with uwsgi (not verified)
uwsgi --http 0.0.0.0:5000 --ini conf/jeffcupdb-{dev|prod}.ini
```

## Update:
```
python -m jeffcupdb.db.update
```


# espn-ffb
espn-ffb is a project to query fantasy football data from ESPN's API and persist it in your own database. There is a very basic web component with a few views built using Flask that allows you to self-host your own fantasy football league page for things such as historical records, weekly recaps, etc.

#### Pre-requisites:
*  Python3
*  Database
*  uWSGI (optional, but recommended if running in production)

## Requirements:
```
pip3 install -r requirements.txt
```

## Config:

Edit [config.py](espn_ffb/config.py) with your own:
*  Enter your database credentials in `DevConfig` and `ProdConfig`.
*  `LEAGUE_ID`
*  `swid` (private leagues)
*  `espn_s2` (private leagues)
  
To find your `swid` and `espn_s2` in Chrome, go to **DevTools > Application > Cookies >** https://fantasy.espn.com.

## Setup:
```
python3 -m espn_ffb.setup -e {dev|prod}
```

## Run:
```
# run with python3
python3 -m espn_ffb.app -e {dev|prod}

# run with uwsgi
uwsgi --http 0.0.0.0:5000 --ini conf/espn-ffb-{dev|prod}.ini
```

## Update:
```
python3 -m espn_ffb.db.update -e {dev|prod}
```

## Build:
```
./gradlew clean build buildDeb -PbuildNumber=local
```

## Install:
```
sudo dpkg -i build/distributions/espn-ffb*.deb
```

The `.deb` package includes two `.service` files:
*  `espn-ffb.service`: Starts espn-ffb Flask app
*  `espn-ffb-update.service`: Updates espn-ffb database
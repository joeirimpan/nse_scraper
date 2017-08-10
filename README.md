# NSE Scraper
A web app displaying real time stocks from NSE.

# Setting up the environment vars

```shell
export REDIS_URL=redis://localhost:6379/0
```

# Installation

Then run the following commands to bootstrap your environment.

```shell
git clone git@github.com:joeirimpan/nse_scraper.git
cd nse_scraper
mkvirtualenv -a $(pwd) ${PWD##*/}
pip install -r requirements.txt
```

# Running the application
```shell
python serve.py
```

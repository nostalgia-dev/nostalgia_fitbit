# MyFitbit

Because *"Your data belongs to you!"*

...and fitbit's own data export sucks.

![Python version](https://img.shields.io/pypi/pyversions/nostalgia_fitbit.svg?style=flat)
[![Build status](https://img.shields.io/travis/Knio/nostalgia_fitbit/master.svg?style=flat)](https://travis-ci.org/Knio/nostalgia_fitbit)
[![Coverage status](https://img.shields.io/coveralls/github/Knio/nostalgia_fitbit/master.svg?style=flat)](https://coveralls.io/r/Knio/nostalgia_fitbit?branch=master)
[![PyPI version](https://img.shields.io/pypi/v/nostalgia_fitbit.svg?style=flat)](https://pypi.org/project/nostalgia_fitbit/)
[![PyPI downloads](https://img.shields.io/pypi/dm/nostalgia_fitbit.svg?style=flat)](https://pypi.org/project/nostalgia_fitbit/)

## Installation

    pip install nostalgia_fitbit

## Setup

`nostalgia_fitbit` assumes a registered app.

To get started, follow the prompts after running (will open a browser):

    nostalgia_fitbit


The app should look like this:

The Callback URL must be exactly `http://localhost:8189/auth_code`

<img src="docs/fitbit_app.png" width="271" height="606">

Note that the fitbit API is rate limited to 150 calls/hour, and you can query only 1 day of heartrate data at a time. If you many days of data, you will be rate limited and see an HTTP 429 error. Simply re-run the command an hour later and it will resume downloading where it left off.


## Generate report

Note: This is not officially supported by nostalgia

```
python3 -m nostalgia_fitbit.report --user 123ABC
```

Use the user id seen in the output from step 2

This will generate `report.html` in your current working directory.

![Fitbit Report](docs/fitbit.png)

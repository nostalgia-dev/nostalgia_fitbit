import argparse
import configparser
import getpass
import logging
import json
import just
import webbrowser
import getpass

import requests

from nostalgia_fitbit import Fitbit, FitbitAuth
from nostalgia_fitbit.export import FitbitExport

logging.basicConfig(level=logging.DEBUG)


def main():
    conf_path = "~/nostalgia_data/config/fitbit/config.json"
    if not just.exists(conf_path):
        webbrowser.open("https://dev.fitbit.com/apps/new")
        webbrowser.open(
            "https://raw.githubusercontent.com/nostalgia-dev/nostalgia_fitbit/master/docs/fitbit_app.png"
        )
        client_id = getpass.getpass("Client ID: ")
        client_secret = getpass.getpass("Client Secret: ")
        info = {"client_id": client_id, "client_secret": client_secret}
        just.write(info, conf_path)
        print("Saved in:", conf_path)
    config = just.read(conf_path)
    if not config["client_id"] or not config["client_secret"]:
        msg = "Fill in a value for client_id and client_secret in '{}'".format(conf_path)
        raise ValueError(msg)

    fa = FitbitAuth(client_id=config['client_id'], client_secret=config['client_secret'])
    fa.ensure_access_token()

    try:
        f = Fitbit(access_token=fa.access_token['access_token'])
        print(json.dumps(f.profile, indent=2))
    except requests.exceptions.HTTPError as e:
        print(e.response.status_code)
        if e.response.status_code == 429:
            print(e.response.headers)
            return
        raise

    export = FitbitExport(f, profile=f.profile)

    export.sync_sleep()
    export.sync_heartrate_intraday()


if __name__ == '__main__':
    main()

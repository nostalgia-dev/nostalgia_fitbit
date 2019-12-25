import os
import time
import json
import just
import logging
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

log = logging.getLogger(__name__)


class FitbitExport(object):
    def __init__(self, client=None, user_id=None, profile=None):
        self.root = just.make_path("~/nostalgia_data/input/fitbit")
        self.client = client
        self.user_id = user_id
        self.profile = profile
        if profile is not None:
            self.member_since = datetime.strptime(self.profile["memberSince"], "%Y-%m-%d").date()
        else:
            self.member_since = None

    def filename(self, *args):
        u = self.client and self.client.user_id or self.user_id
        return os.path.join(self.root, u, *args)

    @staticmethod
    def write(filename, data):
        dirname = os.path.dirname(filename)
        os.makedirs(dirname, exist_ok=True)
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=2, sort_keys=True))

    def sync_sleep(self):
        date_start = self.member_since.replace(day=1)
        while 1:
            date_end = date_start + relativedelta(months=1)

            if date_start > date.today():
                break

            partial = date_end > date.today()
            partial_filename = self.filename(
                'sleep',
                'sleep.{:04d}.{:02d}.partial.json'.format(date_start.year, date_start.month),
            )
            filename = self.filename(
                'sleep', 'sleep.{:04d}.{:02}.json'.format(date_start.year, date_start.month)
            )

            if os.path.isfile(partial_filename):
                os.remove(partial_filename)

            if partial:
                filename = partial_filename
            if not os.path.isfile(filename):
                log.info('Downloading: %s', filename)
                sleep = self.client.get_sleep_range(date_start, date_end - timedelta(days=1))
                self.write(filename, sleep)
            else:
                log.info('Cached: %s', filename)
            date_start = date_end

    def heartrate_intraday_filenames(self):
        start = self.member_since
        days = 0
        partials = self.filename("heartrate_intraday", "*/*.partial*.json")
        print("partials", partials)
        print("h", just.remove(partials, allow_recursive=True))
        while 1:
            d = start + timedelta(days=days)
            days += 1
            if d > date.today():
                return
            partial = ".partial_{}".format(time.time()) if d == date.today() else ""
            filename = self.filename(
                'heartrate_intraday',
                '{:04d}'.format(d.year),
                'heartrate_intraday.{:04d}.{:02d}.{:02d}{}.json'.format(
                    d.year, d.month, d.day, partial
                ),
            )
            yield d, filename

    def sync_heartrate_intraday(self):
        for d, filename in self.heartrate_intraday_filenames():
            if os.path.isfile(filename):
                log.info('Cached: %s', filename)
                continue

            log.info('Downloading: %s', filename)
            hr = self.client.get_heartrate_intraday(d)
            self.write(filename, hr)

    def get_sleep(self):
        sleep = []
        for dir, dirs, files in os.walk(self.filename('sleep')):
            for file in files:
                filename = os.path.join(dir, file)
                data = json.load(open(filename))
                if not data:
                    continue
                sleep.extend(data)
        return sleep

    def get_heartrate_intraday(self):
        def compress(data):
            minutes = [None] * 24 * 60
            for o in data:
                h, m, s = map(int, o['time'].split(':'))
                i = h * 60 + m
                minutes[i] = o['value']
            return minutes

        heartrate = []
        for d, filename in self.heartrate_intraday_filenames():
            if not os.path.isfile(filename):
                continue
            data = json.load(open(filename))
            if not data:
                continue
            heartrate.append({'date': d.isoformat(), 'minutes': compress(data)})
        return heartrate

"""
Scrapes an API and returns the JSON data
"""
import requests

from common.globals import STARA_API_BASE


class APIScraper(object):
    app_key = ""
    base_url = ""
    headers = {}

    def __init__(self, base_url=STARA_API_BASE, app_key='f848dba8-adc9-45e5-9771-b51b0ffa700a'):
        self.base_url = base_url
        self.app_key = app_key
        self.headers = {
            'appKey': self.app_key,
            'x-thingworx-session': 'true',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get(self, resource, payload=None):
        if payload is None:
            payload = {}
        print("Getting  {}".format(resource))
        r = requests.get(url="{}/{}".format(self.base_url, resource), headers=self.headers, params=payload)
        print(r.json())

    def post(self, resource, payload=None):
        if payload is None:
            payload = {}
        print("Posting  {}".format(resource))
        r = requests.post(url="{}/{}".format(self.base_url, resource), headers=self.headers, params=payload)
        print(r.json())


if __name__ == '__main__':
    scraper = APIScraper()
    scraper.post("Vehicles")

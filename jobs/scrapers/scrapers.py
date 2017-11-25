import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.globals import STARA_API_BASE


class DBConnector(object):
    engine = None
    session = None

    def __init__(self, uri):
        self.engine = create_engine(uri)
        Session = sessionmaker(bind=self.engine)
        self.session = Session(autoflush=True)


""" Scrapes an API and returns the JSON data """


class StaraAPIScraper(object):
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
        r = requests.get(url="{}/{}".format(self.base_url, resource), headers=self.headers, params=payload)
        return r

    def post(self, resource, payload=None):
        if payload is None:
            payload = {}
        r = requests.post(url="{}/{}".format(self.base_url, resource), headers=self.headers, params=payload)
        return r


'''
SumoLogic Model
'''
import config
import json
import logging
import requests
import sumologic

_logger = logging.getLogger(__name__)

SUMOLOGIC_ACCESS_ID = config.SUMOLOGIC_ACCESS_ID
SUMOLOGIC_ACCESS_KEY = config.SUMOLOGIC_ACCESS_KEY

SUMOLOGIC_COLLECTOR_NAME = config.SUMOLOGIC_COLLECTOR_NAME
SUMOLOGIC_COLLECTOR_CATEGORY = config.SUMOLOGIC_COLLECTOR_CATEGORY
SUMOLOGIC_COLLECTOR_DESCRIPTION = config.SUMOLOGIC_COLLECTOR_DESCRIPTION
SUMOLOGIC_SOURCE_NAME = config.SUMOLOGIC_SOURCE_NAME
SUMOLOGIC_SOURCE_HOSTNAME = config.SUMOLOGIC_SOURCE_HOSTNAME
SUMOLOGIC_SOURCE_DESCRIPTION = config.SUMOLOGIC_SOURCE_DESCRIPTION
SUMOLOGIC_SOURCE_CATEGORY = config.SUMOLOGIC_SOURCE_CATEGORY

class SumoLogicModel:
    def __init__(self,
                 access_id=SUMOLOGIC_ACCESS_ID,
                 access_key=SUMOLOGIC_ACCESS_KEY):

        self._sumologic = sumologic.SumoLogic(
            accessId=access_id,
            accessKey=access_key
        )

    def _get_collector_id_by_name(self, collector_name):
        '''Return the collector ID for the given name.'''
        collector_id = None
        collectors = self._sumologic.collectors()
        for c in collectors:
            if c.get('name') == collector_name:
                collector_id = c.get('id')
        return collector_id

    def create_collector(self):
        '''Create collector'''
        collector_data = {}
        collector_data['collector'] = {
            'collectorType': 'Hosted',
            'name': SUMOLOGIC_COLLECTOR_NAME,
            'description': SUMOLOGIC_COLLECTOR_DESCRIPTION,
            'category': SUMOLOGIC_COLLECTOR_CATEGORY
        }

        # This doesn't exist natively in module for some reason.
        r = requests.post(
            self._sumologic.endpoint + '/collectors',
            json=collector_data,
            headers={'Content-Type': 'application/json'},
            auth=(SUMOLOGIC_ACCESS_ID, SUMOLOGIC_ACCESS_KEY)
        )
        return r.json()

    def create_source(self):
        '''Create collector'''
        source = {}
        source['source'] = {
            'name': SUMOLOGIC_SOURCE_NAME,
            'description': SUMOLOGIC_SOURCE_DESCRIPTION,
            'category': SUMOLOGIC_SOURCE_CATEGORY,
            'hostName': SUMOLOGIC_SOURCE_HOSTNAME,
            'messagePerRequest': True,
            'sourceType': 'HTTP',
        }

        collector_id = self._get_collector_id_by_name(
            SUMOLOGIC_COLLECTOR_NAME
        )
        r = self._sumologic.create_source(collector_id, source)
        return r

    def check_collector_exists(self):
        '''check if a collector already exists'''
        exists = False
        collectors = self._sumologic.collectors()
        for c in collectors:
            if c.get('name') == SUMOLOGIC_COLLECTOR_NAME:
                exists = True
        return exists

    def check_source_exists(self):
        '''Check if a source already exists.'''
        exists = False
        collector_id = self._get_collector_id_by_name(
            SUMOLOGIC_COLLECTOR_NAME
        )

        sources = self._sumologic.sources(collector_id)
        for s in sources:
            if s.get('name') ==  SUMOLOGIC_SOURCE_NAME:
                exists = True

        return exists

    def is_available(self):
        '''Check SumoLogic availability'''
        # We'll throw an exception on failure that'll be caught.
        self._sumologic.collectors()
        return True

    def put_alert_event(self, alert):
        '''Put alert data into SumoLogic'''
        collector_id = self._get_collector_id_by_name(SUMOLOGIC_COLLECTOR_NAME)

        sources = self._sumologic.sources(collector_id)
        for s in sources:
            if s.get('name') == SUMOLOGIC_SOURCE_NAME:
                endpoint = s.get('url')

        r = requests.post(
            endpoint,
            json=alert,
            headers={'Content-Type': 'application/json'},
            auth=(SUMOLOGIC_ACCESS_ID, SUMOLOGIC_ACCESS_KEY)
        )

        if r.ok:
            success = True
        else:
            success = False
        return success


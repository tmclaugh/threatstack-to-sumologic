import os
THREATSTACK_API_KEY = os.environ.get('THREATSTACK_API_KEY')
THREATSTACK_BASE_URL = os.environ.get('THREATSTACK_BASE_URL', 'https://app.threatstack.com/api/v1')

SUMOLOGIC_ACCESS_ID = os.environ.get('SUMOLOGIC_ACCESS_ID')
SUMOLOGIC_ACCESS_KEY = os.environ.get('SUMOLOGIC_ACCESS_KEY')


SUMOLOGIC_COLLECTOR_NAME = os.environ.get('SUMOLOGIC_COLLECTOR_NAME',
                                          'Threat Stack')

SUMOLOGIC_COLLECTOR_DESCRIPTION = os.environ.get('SUMOLOGIC_COLLECTOR_DESCRIPTION',
                                                 'Threat Stack Integration')

SUMOLOGIC_COLLECTOR_CATEGORY = os.environ.get('SUMOLOGIC_COLLECTOR_NAME',
                                              'security/threatstack')

SUMOLOGIC_SOURCE_NAME = os.environ.get('SUMOLOGIC_SOURCE_NAME',
                                       'threatstack-to-sumologic')

SUMOLOGIC_SOURCE_HOSTNAME = os.environ.get('SUMOLOGIC_SOURCE_HOSTNAME',
                                           'threatstack-to-sumologic')

SUMOLOGIC_SOURCE_DESCRIPTION = os.environ.get('SUMOLOGIC_SOURCE_DESCRIPTION',
                                              'threatstack-to-sumologic webhook')

SUMOLOGIC_SOURCE_CATEGORY = os.environ.get('SUMOLOGIC_SOURCE_CATEGORY',
                                           'security/threatstack/alert')


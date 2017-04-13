'''
Send alert events to sumologic.
'''

from flask import Blueprint, jsonify, request
import logging
import app.models.sumo as sumologic_model
import app.models.threatstack as threatstack_model
from app.sns import check_aws_sns

_logger = logging.getLogger(__name__)

sumologic = Blueprint('sumologic', __name__)

#decerator refers to the blueprint object.
@sumologic.route('/status', methods=['GET'])
def is_available():
    '''
    Test that Threat Stack and sumologic bucket are reachable.
    '''
    _logger.info('{}: {}'.format(request.method, request.path))
    sl = sumologic_model.SumoLogicModel()
    sumologic_status = sl.is_available()
    sumologic_info = {'success': sumologic_status}

    ts = threatstack_model.ThreatStackModel()
    ts_status = ts.is_available()
    ts_info = {'success': ts_status}

    status_code = 200
    if sumologic_status and ts_status:
        success = True
    else:
        success = False

    return jsonify(success=success, sumologic=sumologic_info, threatstack=ts_info), status_code

@sumologic.route('/event', methods=['POST'])
@check_aws_sns
def put_alert():
    '''
    Archive Threat Stack alerts to sumologic.
    '''
    _logger.info('{}: {} - {}'.format(request.method,
                                      request.path,
                                      request.data))
    sumologic_response_list = []
    # Required to handle SNS requests which do not set Content-Type to
    # application/json.
    webhook_data = request.get_json(force=True)
    for alert in webhook_data.get('alerts'):
        ts = threatstack_model.ThreatStackModel()
        alert_full = ts.get_alert_by_id(alert.get('id'))

        sl = sumologic_model.SumoLogicModel()
        sumologic_response = sl.put_alert_event(alert_full)
        sumologic_response_list.append({alert.get('id'): sumologic_response})

    status_code = 200
    success = True
    response = {'success': success, 'sumologic': sumologic_response_list}

    return jsonify(response), status_code


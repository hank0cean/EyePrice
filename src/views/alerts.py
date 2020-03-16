import json
from flask import Blueprint
from models.alert import Alert

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/new', methods=['GET', 'POST'])
def new_alert():
    return "<h1>Hello new alert</h1>"

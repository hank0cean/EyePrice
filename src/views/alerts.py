import json
from flask import Blueprint, request, render_template
from models.item import Item
from models.alert import Alert

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/new', methods=['GET', 'POST'])
def new_alert():
    if request.method == 'POST':
        item_id = request.form['item_id']
        price_limit = request.form['price_limit']
        if Item.get_by_id(item_id) is not None:
            Alert(item_id, price_limit).save_to_mongo()
    return render_template('alerts/new_alert.html')

@alert_blueprint.route('/all', methods=['GET'])
def all_alerts():
    alerts = Alert.all()
    return render_template('alerts/all_alerts.html', alerts=alerts)

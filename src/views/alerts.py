import json
from flask import Blueprint, redirect, request, render_template, url_for
from models.item import Item
from models.alert import Alert

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/new/<string:item_id>', methods=['GET', 'POST'])
def new_alert(item_id):
    if Item.get_by_id(item_id) is not None:
        if request.method == 'POST':
            price_limit = request.form['price_limit']
            Alert(item_id, price_limit).save_to_mongo()
            return redirect(url_for('alerts.all_alerts'))
        item = Item.get_by_id(item_id)
        return render_template('alerts/new_alert.html', item=item)
    else:
        return render_template('items/all_items.html')

@alert_blueprint.route('/all', methods=['GET'])
def all_alerts():
    alerts = Alert.all()
    return render_template('alerts/all_alerts.html', alerts=alerts)

from flask import Blueprint, request, render_template
from models.item import Item
from models.alert import Alert
from models.store import Store

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/new', methods=['GET', 'POST'])
def new_alert():
    if request.method == 'POST':
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])
        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)
        item.save_to_mongo()
        Alert(item._id, item_url, price_limit).save_to_mongo()
    return render_template('alerts/new_alert.html')

@alert_blueprint.route('/all', methods=['GET'])
def all_alerts():
    alerts = Alert.all()
    for alert in alerts:
        alert.load_item_price()
    return render_template('alerts/all_alerts.html', alerts=alerts)

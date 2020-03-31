from flask import Blueprint, redirect, render_template, request, url_for
from models.item import Item
from models.alert import Alert
from models.store import Store

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/new', methods=['GET', 'POST'])
def new_alert():
    if request.method == 'POST':
        name = request.form['name']
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'])
        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query, name)
        item.load_price()
        item.save_to_mongo()
        Alert(item._id, price_limit).save_to_mongo()
        return redirect(url_for('.all_alerts'))
    return render_template('alerts/new_alert.html')

@alert_blueprint.route('/edit', methods=['GET'])
@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert is not None:
        if request.method == 'POST':
            new_price_limit = float(request.form['price_limit'])
            alert.price_limit = new_price_limit
            alert.save_to_mongo()
            return redirect(url_for('.all_alerts'))
        return render_template('alerts/edit_alert.html', alert=alert)
    else:
        return redirect(url_for('.all_alerts'))

@alert_blueprint.route('/delete/<string:alert_id>')
def delete_alert(alert_id):
    Alert.get_by_id(alert_id).remove_from_mongo()
    return redirect(url_for('.all_alerts'))

@alert_blueprint.route('/', methods=['GET'])
@alert_blueprint.route('/all', methods=['GET'])
def all_alerts():
    alerts = Alert.all()
    for alert in alerts:
        alert.item.load_price()
    return render_template('alerts/all_alerts.html', alerts=alerts)

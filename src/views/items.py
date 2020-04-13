import json
from flask import Blueprint, render_template, request

from models.item import Item
from models.user.decorators import requires_login

item_blueprint = Blueprint('items', __name__)

@item_blueprint.route('/new', methods=['GET', 'POST'])
@requires_login
def new_item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        url = request.form['url']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])
        item = Item(url, tag_name, query, item_name)
        if item:
            item.save_to_mongo()
    return render_template('items/new_item.html')

@item_blueprint.route('/all', methods=['GET'])
@requires_login
def all_items():
    items = Item.all()
    for item in items:
        item.load_price()
    return render_template('items/all_items.html', items=items)

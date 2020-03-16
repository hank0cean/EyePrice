import json
from flask import Blueprint, render_template, request
from models.item import Item

item_blueprint = Blueprint('items', __name__)

@item_blueprint.route('/new', methods=['GET', 'POST'])
def new_item():
    if request.method == 'POST':
        url = request.form['url']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])
        # Item.validate(url, tag_name, query).save_to_mongo()

        Item(url, tag_name, query).save_to_mongo()

    return render_template('items/new_item.html')

@item_blueprint.route('/new/steam', methods=['GET', 'POST'])
def new_steam_item():
    if request.method == 'POST':
        url = request.form['url']
        tag_name = 'div'
        query = {"class": "game_purchase_price price"}

        Item(url, tag_name, query).save_to_mongo()

    return render_template('items/new_steam_item.html')

@item_blueprint.route('/all', methods=['GET'])
def all_items():
    items = Item.all()
    return render_template('items/all_items.html', items=items)


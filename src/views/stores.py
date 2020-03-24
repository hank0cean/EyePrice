from flask import Blueprint, render_template, request
import json

from models.store import Store

store_blueprint = Blueprint('stores', __name__)

@store_blueprint.route('/new', methods=['GET', 'POST'])
def new_store():
    if request.method == 'POST':
        store = Store(name=request.form['store_name'],
                      url_prefix=request.form['url'],
                      tag_name=request.form['tag_name'],
                      query=json.loads(request.form['query']))
        if store:
            store.save_to_mongo()
    return render_template('stores/new_store.html')


@store_blueprint.route('/all', methods=['GET'])
def all_stores():
    pass
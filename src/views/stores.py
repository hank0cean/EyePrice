from flask import Blueprint, redirect, render_template, request, url_for
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

@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
def edit_store(store_id):
    store = Store.get_by_id(store_id)
    if store is not None:
        if request.method == 'POST':
            new_url_prefix = request.form['url_prefix']
            new_tag_name = request.form['tag_name']
            new_query = request.form['query']
            store.url_prefix = new_url_prefix
            store.tag_name = new_tag_name
            store.query = new_query
            store.save_to_mongo()
            return redirect(url_for('.all_stores'))
        return render_template('stores/edit_store.html', store=store)
    else:
        return redirect(url_for('.all_stores'))

@store_blueprint.route('/delete/<string:store_id>')
def delete_store(store_id):
    Store.get_by_id(store_id).remove_from_mongo()
    return redirect(url_for('.all_stores'))

@store_blueprint.route('/', methods=['GET'])
@store_blueprint.route('/all', methods=['GET'])
def all_stores():
    stores = Store.all()
    return render_template('stores/all_stores.html', stores=stores)

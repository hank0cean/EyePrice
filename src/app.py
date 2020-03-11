from flask import Flask, render_template, request
from models.item import Item

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/new_item', methods=['GET', 'POST'])
def new_item():
    if request.method == 'POST':
        url = request.form['url']
        tag_name = request.form['tag_name']
        query = request.form['query']

        Item(url, tag_name, query).save_to_mongo()

    return render_template('new_item.html')

@app.route('/steam', methods=['GET', 'POST'])
def new_steam_item():
    if request.method == 'POST':
        url = request.form['url']
        tag_name = 'div'
        query = {"class": "game_purchase_price price"}

        Item(url, tag_name, query).save_to_mongo()

    return render_template('new_steam_item.html')

@app.route('/items', methods=['GET'])
def list_items():
    items = Item.all()
    return render_template('list_items.html', items=items)


if __name__ == "__main__":
    app.run(debug=True)

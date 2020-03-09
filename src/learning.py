from flask import Blueprint

learning_blueprint = Blueprint('learning', __name__)


@learning_blueprint.route('/<string:name>')
def home(name):
    return f"Hello {name}"

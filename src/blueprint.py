from flask import Blueprint

blueprint = Blueprint('learning', __name__)


@blueprint.route('/<string:name>')
def home(name):
    return f"Hello {name}"

from flask import Blueprint
from .models import Boy

vehicles = Blueprint('vehicles', 'vehicles', url_prefix='/api/vehicles')


@vehicles.route('/boys/<int:user_id>')
def hello_world(user_id):
    try:
        name = Boy.query.get(user_id).name
        return "<h1>Hello, {}</ht>".format(name)
    except Exception as ex:
        print(ex)
        return '<h1>Something is broken.</h1>'


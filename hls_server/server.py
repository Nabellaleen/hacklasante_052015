from flask import render_template
from flask import request, jsonify, abort

import flask.views

from hls_server.database import get_database
from hls_server.user import User

class HlsServerView(flask.views.MethodView):
    def get(self):
        return render_template('main.html')

def rest_user(user_id=None):
    database = get_database()
    request_method = request.method
    if request_method == 'GET':
        try:
            user = database.get_user(user_id)
        except KeyError:
            abort(404)
        return jsonify(user.get_namespace())

    elif request_method == 'PUT':
        json_data = request.get_json(force=True)
        try:
            user = database.get_user(user_id)
        except KeyError:
            abort(404)
        for key, value in json_data['fields'].items():
            user.set_value(key, value)
        return jsonify(user.get_namespace())

    elif request_method == 'POST':
        json_data = request.get_json(force=True)
        {'fields': {'birthyear': 1988, 'name': 'Florian'}}
        new_user = User()
        for key, value in json_data['fields'].items():
            new_user.set_value(key, value)
        new_user = database.add_user(new_user)
        return jsonify(new_user.get_namespace())

    elif request_method == 'DELETE':
        deleted_user = database.pop_user(user_id)
        return jsonify(deleted_user.get_namespace())
    abort(405)

def get_users():
    json_data = request.get_json(force=True)
    database = get_database()
    users = database.search_users(json_data['fields'])
    users_ns = []
    for user in users:
        user_json = user['user'].get_basic_namespace()
        users_ns.append({'user': user_json,
                         'score': user['score']})

    missing_fields = database.get_missing_fields(
        fields=json_data['fields'].keys(),
        users=users)
    missing_fields_ns = []
    for field in missing_fields:
        field_json = {
            'name': field['name'],
            'weight': field['field'].get_weight()}
        missing_fields_ns.append(field_json)

    return jsonify(
            users=users_ns,
            missing_fields=missing_fields_ns
        )

from flask import render_template
from flask import request, jsonify, abort

import flask.views

from hls_server.database import get_database

class HlsServerView(flask.views.MethodView):
    def get(self):
        return render_template('main.html')

def rest_user(user_id):
    database = get_database()
    try:
        user = database.get_user(user_id)
    except KeyError:
        abort(403)
    if not user:
        abort(402)
    request_method = request.method
    if request_method == 'GET':
        return jsonify(user.get_namespace())
    elif request_method == 'POST':
        pass
    elif request_method == 'PUT':
        pass
    elif request_method == 'DELETE':
        deleted_user = database.pop_user(user_id)
        return jsonify(deleted_user.get_namespace())
    abort(401)

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

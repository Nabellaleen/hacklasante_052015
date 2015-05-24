from flask import render_template
from flask import request, jsonify

import flask.views

from hls_server.database import get_database

class HlsServerView(flask.views.MethodView):
    def get(self):
        return render_template('main.html')

def get_users():
    json_data = request.get_json(force=True)
    database = get_database()
    users = database.search_users(json_data['fields'])
    missing_fields = database.get_missing_fields(
        fields=json_data['fields'].keys(),
        users=users)

    result = []
    for entry in users:
        user_json = entry['user'].get_namespace()
        result.append({'user': user_json,
                       'score': entry['score']})
    return jsonify(
            users=result,
            missing_fields=missing_fields
        )

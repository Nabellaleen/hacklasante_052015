from flask import Flask

from hls_server.server import HlsServerView, get_users, rest_user
from hls_server.database import init_database, get_database

app = Flask(__name__)

app.add_url_rule('/',
    view_func=HlsServerView.as_view('hls_server_view'),
    methods=['GET'])

app.add_url_rule('/database/;restore',
    view_func=restore_database,
    methods['POST'])

app.add_url_rule('/;get_users',
    view_func=get_users,
    methods=['POST'])

app.add_url_rule('/users',
    view_func=rest_user,
    methods=['POST'])

app.add_url_rule('/users/<user_id>',
    view_func=rest_user,
    methods=['GET', 'PUT', 'DELETE'])

if __name__ == "__main__":
    init_database('data/database.csv')
    app.run(debug=True)

from flask import Flask

from hls_server.server import HlsServerView

app = Flask(__name__)

app.add_url_rule('/',
	view_func=HlsServerView.as_view('hls_server_view'),
    methods=['GET'])

if __name__ == "__main__":
    app.run(debug=True)

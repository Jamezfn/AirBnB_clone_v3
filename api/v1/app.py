#!/usr/bin/python3

from flask import Flask, Response, jsonify
from models import storage
from api.v1.views import app_views
import os
import json
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exec):
    """Closes storage on teardown"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """JSON 404 error handler"""
    return Response(json.dumps({"error": "Not found"}, indent=4), status=404, mimetype='application/json')

@app.errorhandler(400)
def bad_request(error):
    """JSON 400 error handler"""
    return Response(json.dumps({"error": str(error.description)}), status=400, mimetype='application/json')

@app.route('/debug/routes')
def debug_routes():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])

if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)

import json
from flask import Flask, request, render_template, jsonify
from threading import Thread
app = Flask(__name__)


occupancy_of_tables = {}

@app.route('/', methods = ['GET', 'POST'])
def display_home():
    if request.method == 'GET':
        return render_template('index.html') ## some var
    else:
        updated_data = json.loads(request.get_json())
        for locations in updated_data:
            occupancy_of_tables[locations] = updated_data[locations]
            return jsonify("successfully updated data")
        



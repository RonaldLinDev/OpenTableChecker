import json
from flask import Flask, request, render_template, jsonify
from threading import Thread
app = Flask(__name__)



#default values
total_population = 42
west_population = 35
east_population = 7


@app.route('/', methods = ['GET', 'POST'])
def display_home():
    global total_population, west_population, east_population
    if request.method == 'GET':
        return render_template('index.html', total_population = total_population, west_population = west_population, east_population = east_population) ## some var
    else:
        updated_data = json.loads(request.get_json())
        total_population = 42
        west_population = 35
        east_population = 7
        return jsonify("successfully updated data")
        



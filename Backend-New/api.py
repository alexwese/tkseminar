from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
import logging
from Node import Node
import json
from main import *
from pathlib import Path

app = Flask(__name__)
cors = CORS(app)
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

@app.route('/calculate_price', methods=['POST'])



def calculate_price():
    nodes_list = []
    node_objs = []
    result = 0
    content = request.json
    logging.info(content)
    nodes = content['nodes']

    for i in nodes:
        nodes_list.append(Node(i['node_id'], i['name'], i['base_val'], i['coefficient'], i['input_nodes']))


    for obj in nodes_list:
        node_objs.append(obj)
        logging.info(obj.name)

# Integrate user inputs of expected values
    inputs = content['inputs']
    for i in inputs:
        if i['expected_val'] != 0:
            for node in node_objs:
                if node.node_id == i['node_id']:
                    logging.info(node.impact)
                    node.set_expected_val(i['expected_val'])
                    logging.info(node.impact)
                    logging.info("found")
        build_network(node_objs)

    for i in node_objs:
        if(i.name == "aluminium price"):
            result = i.expected_val
    return jsonify(result)

@app.route('/build_network', methods=['GET'])

def build_network():

    p = Path(__file__).with_name('new_risk_data.json')
    filename = p.absolute()

    file = open(filename)
    base_network = json.load(file)
    file.close()
    return base_network

@app.route('/calculate_result', methods=['POST'])

def  calculate_result():
    content = request.json
    logging.info(content)
    nodes = content['children']
    flag = False


    for i in nodes:
        if i["attributes"]['expected_change'] != None:
            flag = True
        if "children" in i:
            for j in i['children']:
                if j["attributes"]["expected_change"] != None:
                    flag = True

    if flag == False:
        return jsonify(content)
    else:
        pass


if __name__ == '__main__':
    app.run(host='localhost',port=8080)




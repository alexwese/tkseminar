from flask import Flask,request,jsonify
import pandas as pd
import logging
from Node import Node
from NewNode import NewNode
import json
from json import JSONEncoder
from main import *

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
            return o.__dict__

app = Flask(__name__)
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

@app.route('/calculate', methods=['POST'])

def calculate():
    content = request.json
    network = json.load(open("risk_data.json"))
    inputs = content['inputs']
    nodes = network['children']
    nodes_list = []

    for i in nodes:
        if "children" in i:
            child_list = []
            new_node = NewNode(i['attributes']['node_id'], i['name'], i['attributes']['absolute_val'],
                                      i['attributes']['base_val'], i['attributes']['expected_change'],
                                      i['attributes']['coefficient'], [])
            for j in i['children']:
                child_list.append(NewNode(j['attributes']['node_id'], j['name'], j['attributes']['absolute_val'],
                                      j['attributes']['base_val'], j['attributes']['expected_change'],
                                      j['attributes']['coefficient'], []))
            new_node.add_child(child_list)
            nodes_list.append(new_node)
        else:
            nodes_list.append(NewNode(i['attributes']['node_id'], i['name'], i['attributes']['absolute_val'],
                                      i['attributes']['base_val'], i['attributes']['expected_change'],
                                      i['attributes']['coefficient'], []))
    result = []
    for i in inputs:
        for obj in nodes_list:
            if i['node_id'] == obj.node_id:
                logging.info(obj.name)
                obj.set_expected_change(i['expected_change'])
                logging.info(obj.cal_absolute_value())
                break
            if obj.children:
                for child in obj.children:
                    if i['node_id'] == child.node_id:
                        logging.info(child.name)
                        logging.info(child.impact)
                        child.set_expected_change(i['expected_change'])
                        logging.info(child.impact)
                        logging.info(obj.cal_absolute_value())

# final update for all nodes
    for node in nodes_list:
        node.cal_absolute_value()
        result = json.dumps(node, cls=CustomEncoder)
    return jsonify(result)



@app.route('/build_network', methods=['GET'])

def build_network():
    base_network = json.load(open("risk_data.json"))
    return base_network





if __name__ == '__main__':
    app.run(host='localhost',port=8080)




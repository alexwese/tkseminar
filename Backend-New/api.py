from flask import Flask,request,jsonify
import pandas as pd
import logging
from Node import Node
from main import *

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

if __name__ == '__main__':
    app.run(host='localhost',port=8080)




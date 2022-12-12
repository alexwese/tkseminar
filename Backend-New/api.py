from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
import logging
from Node import Node
import json
from json import JSONEncoder
from main import *
from pathlib import Path

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
            return o.__dict__

app = Flask(__name__)
cors = CORS(app)
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)


def create_network_objects(content):
    
    #First Level
    aluminium_node = Node(content['attributes']['node_id'], content['name'], content['attributes']['new_expected_value'],
                                      content['attributes']['initial_regression_value'], content['attributes']['expected_change'],
                                      content['attributes']['coefficient'],content['attributes']['intercept'], [])
    
    #Second Level
    nodes = content['children']
    for i in nodes:

        #Third Level
        if "children" in i:
            
            new_node = Node(i['attributes']['node_id'], i['name'], i['attributes']['new_expected_value'],
                                      i['attributes']['initial_regression_value'], i['attributes']['expected_change'],
                                      i['attributes']['coefficient'],i['attributes']['intercept'], [])
            for j in i['children']:
                cnode = Node(j['attributes']['node_id'], j['name'], j['attributes']['new_expected_value'],
                                      j['attributes']['initial_regression_value'], j['attributes']['expected_change'],
                                      j['attributes']['coefficient'],j['attributes']['intercept'], [])
                new_node.add_child(cnode)
            aluminium_node.add_child(new_node)
            
        else:
            new_node = Node(i['attributes']['node_id'], i['name'], i['attributes']['new_expected_value'],
                                      i['attributes']['initial_regression_value'], i['attributes']['expected_change'],
                                      i['attributes']['coefficient'],i['attributes']['intercept'], [])
    
            aluminium_node.add_child(new_node)

    return aluminium_node
    
    
    
def recalculate_regression_for_network(node):

    secondlevel = node.get_children()
    #2 Level
    for i in secondlevel:
        

        if i.get_children():
            logging.info(i.name)
            i.cal_new_expected_value()
            logging.info(i.new_expected_value)
    
    #Aluminium Node
    node.cal_new_expected_value()
    print(node.new_expected_value)




def update_network(node,node_id,value):
    
    n = get_node_byID(node,node_id)
    n.set_expected_change(value)
    recalculate_regression_for_network(node)
    

    
def get_node_byID(root,id):

    if root.node_id == id:
        return root
    else:
        root = root.get_children()

        for i in root:

            if i.node_id == id:
                return i
            else:
                if i.children:

                    for j in i.children:

                        if j.node_id == id:
                            return j

    return None



def create_json(node):

    pass










@app.route('/calculate', methods=['POST'])
def calculate():
    content = request.json
    #i = build_network()
    inputs = content['inputs']
    aluminium_node = Node(i['attributes']['node_id'], i['name'], i['attributes']['absolute_val'],
                                      i['attributes']['base_val'], i['attributes']['expected_change'],
                                      i['attributes']['coefficient'], [])
    nodes = i['children']
    nodes_list = []

    for i in nodes:
        if "children" in i:
            child_list = []
            new_node = Node(i['attributes']['node_id'], i['name'], i['attributes']['absolute_val'],
                                      i['attributes']['base_val'], i['attributes']['expected_change'],
                                      i['attributes']['coefficient'], [])
            for j in i['children']:
                child_list.append(Node(j['attributes']['node_id'], j['name'], j['attributes']['absolute_val'],
                                      j['attributes']['base_val'], j['attributes']['expected_change'],
                                      j['attributes']['coefficient'], []))
            new_node.add_child(child_list)
            nodes_list.append(new_node)
        else:
            nodes_list.append(Node(i['attributes']['node_id'], i['name'], i['attributes']['absolute_val'],
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

    for node in nodes_list:
        node.cal_absolute_value()
        aluminium_node.cal_absolute_value()
    #Construct final network

    result = {"name": aluminium_node.name,
              "attributes": {
                  "node_id": aluminium_node.node_id,
                  "absolute_val": aluminium_node.absolute_val,
                  "base_val": aluminium_node.base_val,
                  "expected_change": aluminium_node.expected_change,
                  "coefficient": aluminium_node.coefficient
              },
              "children": None
              }

#iterate through children


#Add Aluminium children to final json


    # final update for all nodes
    for node in nodes_list:

        result = {"name": node.name,
                  "attributes": {
                    "node_id": node.node_id,
                    "absolute_val": node.absolute_val,
                    "base_val": node.base_val,
                    "expected_change": node.expected_change,
                    "coefficient": node.coefficient
                  },
                  "children": None
                  }


    return jsonify(result)







@app.route('/get_basenetwork', methods=['GET'])
def get_basenetwork():

    p = Path(__file__).with_name('new_risk_data.json')
    filename = p.absolute()

    file = open(filename)
    base_network = json.load(file)
    file.close()

    return base_network





if __name__ == '__main__':
    
    p = Path(__file__).with_name('new_risk_data.json')
    filename = p.absolute()

    file = open(filename)
    base_network = json.load(file)
    file.close()
    alu = create_network_objects(base_network)
    recalculate_regression_for_network(alu)
    d = get_node_byID(alu,3)

    print(1)

    app.run(host='localhost',port=8080)




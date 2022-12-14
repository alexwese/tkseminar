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
    
    
    
def recalculate_allregressions_for_network(node):

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






def update_networknode(root,node_id,value):

    changed_node = get_node_byID(root,node_id)
    changed_node.set_expected_change(value)

    parent = changed_node.get_parent()

    if(parent.node_id == 0):
        new_parent_value = parent.cal_new_expected_value()

    else:
        update_networknode(root,parent,new_parent_value)



def trigger_changes(root,node_id):

    pass



def update_network(root,node_id,value):
    
    n = get_node_byID(root,node_id)
    n.set_expected_change(value)
    recalculate_allregressions_for_network(root)
    

    
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


def read_usernetwork(user):

    if user == 'User1':

        p = Path(__file__).with_name('risk_data_user1.json')
        filename = p.absolute()

        file = open(filename)
        user_network = json.load(file)
        file.close()
    else:
        p = Path(__file__).with_name('risk_data_user2.json')
        filename = p.absolute()

        file = open(filename)
        user_network = json.load(file)
        file.close()


    return user_network






@app.route('/change_network', methods=['POST'])
def change_network():

    content = request.json

    nodeid = content['id']
    expChange = content['expChange']
    user = content['username']

    file = read_usernetwork(user)
    alu = create_network_objects(file)

    update_network(alu,nodeid,expChange)

    # Overwriting of file
    if user == "User1":
        with open('Backend-New/risk_data_user1.json', 'w') as f:
            json.dump(alu.to_json(), f)
    else:
        with open('Backend-New/risk_data_user2.json', 'w') as f:
            json.dump(alu.to_json(), f)

    return jsonify(alu.to_json())









@app.route('/get_basenetwork', methods=['GET'])
def get_basenetwork():

    p = Path(__file__).with_name('new_risk_data.json')
    filename = p.absolute()

    file = open(filename)
    base_network = json.load(file)
    file.close()

    return base_network





@app.route('/get_usernetwork', methods=['GET'])
def get_usernetwork():
    
    return read_usernetwork(request.form['username'])
   








if __name__ == '__main__':
    

    app.run(host='localhost',port=8080)




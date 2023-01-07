from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
import logging
from Node import Node
import json
from pathlib import Path
import mysql.connector


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
                                      content['attributes']['coefficient'],content['attributes']['intercept'],content['attributes']['lvl'], [])
    
    #Second Level
    nodes = content['children']
    for i in nodes:

        #Third Level
        if "children" in i:
            
            new_node = Node(i['attributes']['node_id'], i['name'], i['attributes']['new_expected_value'],
                                      i['attributes']['initial_regression_value'], i['attributes']['expected_change'],
                                      i['attributes']['coefficient'],i['attributes']['intercept'],i['attributes']['lvl'], [])
            for j in i['children']:
                cnode = Node(j['attributes']['node_id'], j['name'], j['attributes']['new_expected_value'],
                                      j['attributes']['initial_regression_value'], j['attributes']['expected_change'],
                                      j['attributes']['coefficient'],j['attributes']['intercept'],j['attributes']['lvl'], [])
                new_node.add_child(cnode)
            aluminium_node.add_child(new_node)
            
        else:
            new_node = Node(i['attributes']['node_id'], i['name'], i['attributes']['new_expected_value'],
                                      i['attributes']['initial_regression_value'], i['attributes']['expected_change'],
                                      i['attributes']['coefficient'],i['attributes']['intercept'],i['attributes']['lvl'], [])
    
            aluminium_node.add_child(new_node)

    return aluminium_node
    
    
#not needed anymore    
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



def get_parent(root, node):

    for child in root.children:
        if(node.node_id == child.node_id):
            return root
        else:

            for rc in root.children:

                for c in rc.children:

                    if (node.node_id == c.node_id):
                        return rc




def update_networknode(root,node_id,value):

    changed_node = get_node_byID(root,node_id)
    changed_node.set_expected_change(value)
    logging.info(changed_node.name + " set to " + str(changed_node.new_expected_value))

    parent = get_parent(root,changed_node)

    if(parent.node_id == 0):
        new_parent_value = parent.cal_new_expected_value()
    else:
        update_networknode_regressions(root,parent.node_id)



def update_networknode_regressions(root,node_id):

    changed_node = get_node_byID(root,node_id)
    changed_node.cal_new_expected_value()
    logging.info(changed_node.name + " regression value set to " + str(changed_node.new_expected_value))

    parent = get_parent(root,changed_node)

    if(parent.node_id == 0):
        new_parent_value = parent.cal_new_expected_value()

    else:
        update_networknode_regressions(root,parent.node_id)


    

    
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


    mydb = mysql.connector.connect(
        host="db",
        port = "3306",
        user="root",
        password="password"
        ) 

    cursor = mydb.cursor()

    query = ("SELECT * FROM tkseminar.network_test WHERE user_id = " +  user[4:])
    cursor.execute(query)

    for (network, user_id, session_id, json_data, basis) in cursor:
        user_network = json_data


    return user_network






@app.route('/change_network', methods=['POST'])
def change_network():

    logging.info("Change network ...")

    content = request.json

    nodeid = content['id']
    expChange = content['expChange']
    user = content['username']

    file = read_usernetwork(user)
    alu = create_network_objects(file)

    update_networknode(alu,nodeid,expChange)

    mydb = mysql.connector.connect(
        host="db",
        port = "3306",
        user="root",
        password="password"
        ) 

    cursor = mydb.cursor()

    json_data = alu.to_json()

    query = ("UPDATE tkseminar.network_test SET json_file '" + json_data + "' WHERE user_id = " + user[4:])
    cursor.execute(query)


    return jsonify(json_data)









@app.route('/get_basenetwork', methods=['GET'])
def get_basenetwork():

    mydb = mysql.connector.connect(
        host="db",
        port = "3306",
        user="root",
        password="password"
        ) 

    cursor = mydb.cursor()

    query = ("SELECT * FROM tkseminar.network_test WHERE basis = 1")
    cursor.execute(query)
    
    for (network, user_id, session_id, json_data, basis) in cursor:
        base_network = json_data


    return base_network


@app.route('/reset_usernetwork', methods=['GET'])
def reset_usernetwork():

    p = Path(__file__).with_name('new_risk_data.json')
    filename = p.absolute()

    file = open(filename)
    base_network = json.load(file)
    file.close()

    user = request.args.get('username')
    
    # Overwriting of file
    if user == "User1":
        with open('Backend-New/risk_data_user1.json', 'w') as f:
            json.dump(base_network, f)
    else:
        with open('Backend-New/risk_data_user2.json', 'w') as f:
            json.dump(base_network, f)


    return base_network





@app.route('/get_usernetwork', methods=['GET'])
def get_usernetwork():
    
    return read_usernetwork(request.args.get('username'))
   








if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host="db",
        port = "3306",
        user="root",
        password="password"
        )

    print(mydb)    

    cursor = mydb.cursor()

    query = ("SELECT * FROM tkseminar.network_test")


    cursor.execute(query)
    for (network, user_id, session_id, j, basis) in cursor:
        print(user_id)


    cursor.close()

    app.run(host='0.0.0.0',port=8080)




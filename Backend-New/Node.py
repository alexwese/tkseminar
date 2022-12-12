import logging

class Node:
    # constructor method
    def __init__(self, node_id, name, new_expected_value, 
                initial_regression_value, expected_change, 
                coefficient,intercept, children):
        self.node_id = node_id
        self.name = name
        self.initial_regression_value = initial_regression_value    # originally set value
        self.new_expected_value = new_expected_value
        self.expected_change = expected_change
        self.coefficient = coefficient
        self.children = children
        self.intercept = intercept



    def set_expected_change(self, new_value):
        self.expected_change = new_value
        logging.info("Changed from " + str(self.new_expected_value) + " to " + str(self.new_expected_value + self.expected_change) )
        self.new_expected_value = self.new_expected_value + self.expected_change


    def backtrack_change_of_children(self):
        
        if self.children:

            for i in self.children:
                
                pass



    def add_child(self, obj):
        self.children.append(obj)



    def get_children(self):
        return self.children


    def cal_new_expected_value(self):
        new_expected_value = 0
        if self.children:
            for node in self.children:
                new_expected_value = new_expected_value + node.new_expected_value * node.coefficient
            
        self.new_expected_value = new_expected_value + self.intercept
        
    

    def to_json(self):

        res = {
            "name": self.name,
            "attributes": {
                "node_id": self.node_id,
                "intercept": None,
                "new_expected_value": self.new_expected_value,
                "initial_regression_value": self.initial_regression_value,
                "expected_change": self.expected_change,
                "coefficient": self.coefficient
            },
            "children":None
        }
        children = []
        if self.children:
            for i in self.children:
                
                c = i.to_json()
                children.append(c)

        res["children"] = children
        return res

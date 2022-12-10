
class Node:
    # constructor method
    def __init__(self, node_id, name, base_val, coefficient, child_nodes):
        self.node_id = node_id
        self.name = name
        self.base_val = base_val    # originally set value
        self.expected_val = 0       # input by user
        self.change = 0
        self.impact = 0
        self.probability = 0
        self.coefficient = coefficient
        self.child_nodes = child_nodes
        self.cal_impact()
    def set_probability(self, probability):
        self.probability = probability

    def set_expected_val(self, expected_val):
        self.expected_val = expected_val
        self.change = self.expected_val - self.base_val
        self.cal_impact()

    def cal_impact(self):
        if self.expected_val != 0:
            self.impact = self.change * self.coefficient
        else:
            self.impact = self.base_val * self.coefficient

    def cal_new_value(self, all_nodes):
        sum_impact = 0
        for node in all_nodes:
            if node.node_id in self.child_nodes:
                sum_impact += node.impact
                print(sum_impact)
        self.expected_val = sum_impact
        return self.expected_val



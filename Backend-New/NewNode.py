
class NewNode:
    # constructor method
    def __init__(self, node_id, name, absolute_val, base_val, expected_change, coefficient, children):
        self.node_id = node_id
        self.name = name
        self.base_val = base_val    # originally set value
        self.absolute_val = absolute_val
        self.expected_change = expected_change
        self.coefficient = coefficient
        self.children = children
        self.impact = 0
        self.cal_impact()

    def set_expected_change(self, new_value):
        self.expected_change = new_value
        self.cal_impact()

    def add_child(self, obj):
        self.children = obj

    def cal_impact(self):
        if self.expected_change != 0:
            self.impact = (self.base_val + self.expected_change) * self.coefficient
        else:
            self.impact = self.absolute_val * self.coefficient
        print(self.name, self.node_id, self.impact)

    def cal_absolute_value(self):
        sum_impact = 0
        if self.children:
            for node in self.children:
                sum_impact = sum_impact + node.impact
            self.absolute_val = sum_impact # + node.intercept
        else:
            self.absolute_val = self.base_val
        return self.absolute_val



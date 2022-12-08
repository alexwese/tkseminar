
from Node import Node
import pandas as pd





def build_network(all_nodes):

    for node in all_nodes:
        node.cal_new_value(all_nodes)


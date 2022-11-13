import Utility.Constant as cons
import json

def getnodedata(node):
    f = open(cons.DATA_FOLDER+cons.DATA_JSON, 'r')
    load = json.load(f)
 
    return load[node]
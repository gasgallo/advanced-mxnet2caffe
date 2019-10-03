import json
from prototxt_basic import *

def write_prototxt(json_path, prototx_path, input_shape):
  with open(json_path) as json_file:    
    jdata = json.load(json_file)
    print(jdata)
  
  with open(prototx_path, "w") as prototxt_file:
    for i_node in range(0,len(jdata['nodes'])):
      node_i = jdata['nodes'][i_node]
      if str(node_i['op']) == 'null' and str(node_i['name']) != 'data':
        continue
      
      print('{}, \top:{}, name:{} -> {}'.format(i_node,node_i['op'].ljust(20),
                                          node_i['name'].ljust(30),
                                          node_i['name']).ljust(20))
      info = node_i
      
      info['top'] = info['name']
      info['bottom'] = []
      info['params'] = []
      for input_idx_i in node_i['inputs']:
        input_i = jdata['nodes'][input_idx_i[0]]
        if str(input_i['op']) != 'null' or (str(input_i['name']) == 'data'):
          info['bottom'].append(str(input_i['name']))
        if str(input_i['op']) == 'null':
          info['params'].append(str(input_i['name']))
          if not str(input_i['name']).startswith(str(node_i['name'])):
            print('           use shared weight -> %s'% str(input_i['name']))
            info['share'] = True

      if str(node_i['op']) == 'UpSampling':
      found = False
      while not found:
        inputs = node_i['inputs']
        for j in range(len(inputs)):
          if 'attrs' in jdata['nodes'][inputs[j][0]]:
            if 'num_filter' in jdata['nodes'][inputs[j][0]]['attrs']:
              info["num_output"] = int(jdata['nodes'][inputs[j][0]]['attrs']['num_filter'])
              info["group"] = info["num_output"]
              found = True
        node_i = jdata['nodes'][inputs[0][0]]

      if str(node_i['op']) == 'data':
      for char in ['[', ']', '(', ')']:
        input_shape = input_shape.replace(char, '')
      input_shape = [int(item) for item in input_shape.split(',')]
      info["shape"] = input_shape
        
      write_node(prototxt_file, info)
  
  print("*** JSON to PROTOTXT FINISH ***")


# from flask import Flask
#   app = Flask(__name__)
#   app.debug = True
  
#   @app.route('/')
#   def main_method():
#     return "Hello everyone"
  
#   if __name__ == '__main__':
#     app.run()

from flask import Flask
import sys
import socket
import json
import yaml

app = Flask(__name__)
app.debug = True

ip_address = str(socket.gethostbyname(socket.gethostname()))
yaml_file = sys.argv[1]
with open(yaml_file, 'r') as ymlfile:
  cfg = yaml.load(ymlfile)
base_path = cfg['basePath']
consumes = cfg['consumes']
produces = cfg['produces']

# @app.route('/')
# def main_method():
#   return "Hello everyone"

# @app.route('/fun/urls/<param>')
# def fun_url(param=None):
#   return "Parameter passed is: " + param + "\n"



# for section in cfg:
#   print(section)

@app.route(base_path + '/hello', methods=['POST'])
def main_hello():
  ref = cfg['paths']['/hello']['post']['parameters'][0]['schema']['$ref']
  return json.dumps(json_build(ref))

# @app.route(base_path + '/plus_one/<val>', methods=['GET'])
# def main_plus(val):

def json_build(ref):
  data = {}
  model = ref.split("/")[2]
  properties = cfg['definitions'][model]['properties']
  keys = cfg['definitions'][model]['properties'].keys()
  for key in keys:
    if (properties[key]['type'] == 'string'):
      data[key] = "string"
  return data

if __name__ == '__main__':
  app.run(port=80)
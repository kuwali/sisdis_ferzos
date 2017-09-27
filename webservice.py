
from flask import Flask, request, Response
import sys
import socket
import requests
import json
import yaml

ip_address = str(socket.gethostbyname(socket.gethostname()))
yaml_file = sys.argv[1]
with open(yaml_file, 'r') as ymlfile:
  cfg = yaml.load(ymlfile)
base_path = cfg['basePath']
api_version = float(cfg['info']['version'])
consumes = cfg['consumes']
produces = cfg['produces']
service_api = "http://172.17.0.70:17088"

app = Flask(__name__)
app.debug = True

@app.errorhandler(405)
def page_not_found(e):
  response = {}
  response['detail'] = ""
  response['status'] = "405"
  response['title'] = "Method Not Implemented"
  return json.dumps(response, ensure_ascii=True)+"\n", 405

@app.route(base_path + '/hello', methods=['POST'])
def main_hello():
  response = {}
  try:
    data = json.loads(request.data.decode())
    r = requests.get(service_api).text
    r_json = json.loads(r)
    flag = checkRequest(data)
    if flag == 0:
      response['detail'] = "'request' is a required property"
      response['status'] = "400"
      response['title'] = "Bad Request"
      return Response(json.dumps(response, ensure_ascii=True)+"\n", status=400)
    elif flag == 1:    
      response['detail'] = "Value in 'request' must be Integer"
      response['status'] = "400"
      response['title'] = "Bad Request"
      return Response(json.dumps(response, ensure_ascii=True)+"\n", status=400)
    else:
      file = open('count.txt', 'r')
      counter = int(file.read())
      counter = counter + 1
      file = open('count.txt', 'w')
      file.write(str(counter))
      response['response'] = "Good "+ r_json['state'] + ", " + data['request']
      response['currentvisit'] = r_json['datetime']
      response['count'] = counter
      response['apiversion'] = api_version
      return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200)
  except:
    response['detail'] = "Payload must be a valid JSON"
    response['status'] = "400"
    response['title'] = "Bad Request"
    return Response(json.dumps(response, ensure_ascii=True)+"\n", status=400)

@app.route(base_path + '/plus_one/<val>', methods=['GET'])
def main_plus(val):
  valid = checkValue(val)
  response = {}
  if valid:
    response['plusoneret'] = int(val) + 1
    response['apiversion'] = api_version
    return Response(json.dumps(response, ensure_ascii=True)+"\n", status=200)
  else:
    response['detail'] = "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again."
    response['status'] = "404"
    response['title'] = "Not Found"
    return Response(json.dumps(response, ensure_ascii=True)+"\n", status=404)

@app.route(base_path + '/spesifikasi.yaml', methods=['GET'])
def send_yaml():
  file = open('spesifikasi.yaml', 'r')
  return str(file.read())

def checkRequest(json):  
  if 'request' not in json:
    return 0;  
  elif not isinstance(json['request'], str):
    return 1;

def checkValue(val):  
  try:
    int_value = int(val)
    return int_value > -1
  except:
    return False
  
if __name__ == '__main__':
  app.run(ip_address, port=8080)
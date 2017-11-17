import os, requests, json

#Get Admin Token
OS_AUTH_URL = http://180.210.14.102:5000/
TOKEN_REQ_URL = OS_AUTH_URL + '/v3/auth/tokens?nocatalog'
token_req_headers = {'Content-Type': 'application/json'}
token_req_data = {'auth': { 'identity': { 'methods': ['password'],'password': {'user': {'domain': {'name': 'Default'},'name': 'admin', 'password': 'DevStack2017'} } }, 'scope': { 'project': { 'domain': { 'name': 'Default'}, 'name':  'admin' } } }}
token_response = requests.post(TOKEN_REQ_URL, headers=token_req_headers, data=json.dumps(token_req_data))
token = token_response.headers['X-Subject-Token']

#Upload MNIST Model 
API_URL = 'http://180.210.14.172:9000/savedmodel/' + 'mnist' + '/' + '1'
file_name = './1.tar.gz'
savedmodel_req_headers = {'X-AUTH-TOKEN': token, 'content-disposition': 'attachment; filename=' + file_name}
savedmodel_req_data = {'file': open(file_name, 'rb')}
savedmodel_response = requests.post(API_URL, headers=savedmodel_req_headers, files=savedmodel_req_data)

#Change the Model for Serving Cluster
API_URL = 'http://180.210.14.172:9000/serving' + '/' + 'k8s-gpu-cluster' + '/' + 'devstack'
req_headers = {'X-AUTH-TOKEN': token, "Content-Type": "application/json"}
data = { "add_model": { "models" : 'mnist' } }
response = requests.put(API_URL, headers=req_headers, data=json.dumps(data))

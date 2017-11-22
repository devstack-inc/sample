import os, requests, json, sys, time

cluster_name = 'k8s-gpu-cluster'
application_name = 'devstack'
model_name = 'mnist'
version = '1'

os.system('python mnist_saved_model.py --training_iteration=20000 --model_version=1 ./')




if os.path.isdir('./1'):
    os.system('tar zcf 1.tar.gz 1')

    # Get Admin Token
    OS_AUTH_URL = 'http://180.210.14.102:5000/'
    TOKEN_REQ_URL = OS_AUTH_URL + '/v3/auth/tokens?nocatalog'
    token_req_headers = {'Content-Type': 'application/json'}
    token_req_data = {'auth': {'identity': {'methods': ['password'], 'password': {
        'user': {'domain': {'name': 'Default'}, 'name': 'admin', 'password': sys.argv[1]}}},
                               'scope': {'project': {'domain': {'name': 'Default'}, 'name': 'admin'}}}}
    token_response = requests.post(TOKEN_REQ_URL, headers=token_req_headers, data=json.dumps(token_req_data))
    token = token_response.headers['X-Subject-Token']

    # Upload MNIST Model
    API_URL = 'http://180.210.14.103:9000/savedmodel/' + model_name + '/' + version
    file_name = version + '.tar.gz'
    savedmodel_req_headers = {'X-AUTH-TOKEN': token, 'Content-Disposition': 'attachment;filename=' + file_name,
                              "Content-Type": "application/x-gzip"}
    savedmodel_req_data = open(file_name, 'rb')
    savedmodel_response = requests.post(API_URL, headers=savedmodel_req_headers, data=savedmodel_req_data)

    # add New Model for Serving Cluster
    API_URL = 'http://180.210.14.103:9000/serving' + '/' + cluster_name + '/' + application_name
    req_headers = {'X-AUTH-TOKEN': token, "Content-Type": "application/json"}
    data = {"add_model": {"models": 'mnist'}}
    response = requests.put(API_URL, headers=req_headers, data=json.dumps(data))



else:
    os.system('tar zcf 2.tar.gz 2')

    # Get Admin Token
    OS_AUTH_URL = 'http://180.210.14.102:5000/'
    TOKEN_REQ_URL = OS_AUTH_URL + '/v3/auth/tokens?nocatalog'
    token_req_headers = {'Content-Type': 'application/json'}
    token_req_data = {'auth': { 'identity': { 'methods': ['password'],'password': {'user': {'domain': {'name': 'Default'},'name': 'admin', 'password': sys.argv[1]} } }, 'scope': { 'project': { 'domain': { 'name': 'Default'}, 'name':  'admin' } } }}
    token_response = requests.post(TOKEN_REQ_URL, headers=token_req_headers, data=json.dumps(token_req_data))
    token = token_response.headers['X-Subject-Token']

    # Upload MNIST Model
    API_URL = 'http://180.210.14.103:9000/savedmodel/' + model_name + '/' + version
    file_name = version + '.tar.gz'
    savedmodel_req_headers = {'X-AUTH-TOKEN': token, 'Content-Disposition': 'attachment;filename=' + file_name, "Content-Type": "application/x-gzip"}
    savedmodel_req_data = open(file_name, 'rb')
    savedmodel_response = requests.post(API_URL, headers=savedmodel_req_headers, data=savedmodel_req_data)

    # Remove Previous Model
    API_URL = 'http://180.210.14.103:9000/serving' + '/' + cluster_name + '/' + application_name
    req_headers = {'X-AUTH-TOKEN': token, "Content-Type": "application/json"}
    data = {"remove_model": {"models": 'mnist'}}
    response = requests.put(API_URL, headers=req_headers, data=json.dumps(data))

    # Add New Model for Serving Cluster
    API_URL = 'http://180.210.14.103:9000/serving' + '/' + cluster_name + '/' + application_name
    req_headers = {'X-AUTH-TOKEN': token, "Content-Type": "application/json"}
    data = { "add_model": { "models" : 'mnist' } }
    response = requests.put(API_URL, headers=req_headers, data=json.dumps(data))



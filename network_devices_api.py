"""
Author: Sami Nofal 
Date: May, 2022
Aplication Prgramming Interface (API) for Network Devices API
"""
from flask import Flask, request, jsonify
import pickledb
import json
import os

nda = Flask(__name__)
env = os.environ.copy()
path_to_db = os.getcwd()
if 'PROD' in env:
    path_to_db +="/network_devices.db"
else:
    path_to_db +="/tests/test_network_devices.db"

print(path_to_db)
networkDevicesDB = pickledb.load(path_to_db, True, False)
valid_network_device_models = ['ios-xr','ios-xe','nx-os']

# Helper Functions:
"""
is_key_valid
@Description:
    Keys are only valid if the key length is less than 16
"""
def is_key_valid(key):
    if key and len(key)>0 and len(key)<16:
        return True
    return False

"""
is_data_valid
@Description:
    Data is valid if model is part of data and is part of the valid models
    Version is optional
"""
def is_data_valid(data):
    if data and 'model' in data and data['model'] in valid_network_device_models:
        if len(data['version']) > 1000:
            return False
        return True
    return False

"""
extract_key
@Description:
    Returns the fqdn key from json data object if available
"""
def extract_key(obj_json):
    key = None
    if obj_json and 'fqdn' in obj_json:
        key = obj_json['fqdn']
    return key

"""
is_input_valid
@Description:
    Validates the input and makes sure rules are set
"""
def is_input_valid(data, key=None):
    data_valid = is_data_valid(data)

    if data_valid and key == None:
        key = extract_key(data)

    key_valid = is_key_valid(key)

    if key_valid and data_valid:
        return True
    else:
        return False

"""
extract_key_and_data
@Description:
    After the input is validated we extract the key and data
    if key it is an update the key will be part of the path in the redirection
"""
def extract_key_and_data(obj_json, key=None):
    if not key:
        key = obj_json['fqdn']
    data = {}
    data['model'] = obj_json['model']
    if 'version' in obj_json:
        data['version'] = obj_json['version']
    else:
        data['version'] = ""
    return key, data

"""
add_or_update_network_device
@Description:
    Adds or updates the network device in DB 
    ** This is called after ALL data and keys are validated **
"""
def add_or_update_network_device(key, data):

    returnCode = 200 if networkDevicesDB.get(key) else 201
    
    networkDevicesDB.set(key, data)
    return networkDevicesDB.get(key), returnCode


"""
get_network_devices_all
@Description:
    Returns all the network devices available in the database
"""
@nda.get("/v1/network_devices")
def get_network_devices_all():
    keys=networkDevicesDB.getall()
    res = []
    for k in keys:
        res.append({k:networkDevicesDB.get(k)})
    return jsonify(res)

"""
get_network_device
@Description:
    returns network device with key fqdn and 200 if available
    returns 404 if not found
"""
@nda.get("/v1/network_devices/<fqdn>")
def get_network_device(fqdn):
    key = str(fqdn)
    if not is_key_valid(key):
        return {"error": "Invalid input arguments fqdn invalid"}, 400

    db_value = networkDevicesDB.get(key)
    if db_value != False:
        return db_value, 200
    return {},404

"""
add_network_device
@Description:
    Adds or updates network device with key fqdn from Data and 200 if successful
    returns 400 invalid input was given
"""
@nda.post("/v1/network_devices")
def add_network_device():
    if request.is_json:
        obj_json = request.get_json()
        if is_input_valid(obj_json):
            key, data = extract_key_and_data(obj_json)
            return add_or_update_network_device(key,data)
        else:
            return {"error": f"Invalid input arguments key or data invalid" }, 400
    else:
        return {"error": "Request must be JSON"}, 400

"""
update_network_device
@Description:
    Adds or updates network device with key fqdn from PATH and 200 if successful
    returns 400 invalid input was given
"""
@nda.put("/v1/network_devices/<fqdn>")
def update_network_device(fqdn):
    if request.is_json:
        obj_json = request.get_json()
        fqdn_s = str(fqdn)
        if is_input_valid(obj_json, fqdn_s):
            key, data = extract_key_and_data(obj_json, fqdn_s)
            return add_or_update_network_device(key,data)
        else:
            return {"error": f"Invalid input arguments key or data invalid" }, 400
    else:
        return {"error": "Request must be JSON"}, 400

"""
delete_network_device
@Description:
    Deletes network device with key fqdn from PATH and 200 if successful
    returns 400 invalid key was given
    returns 200(OK) if object was not found
"""
@nda.delete("/v1/network_devices/<fqdn>")
def delete_network_device(fqdn):
    key = str(fqdn)
    if not is_key_valid(key):
        return {"error": "Invalid input arguments fqdn invalid"}, 400

    db_value = networkDevicesDB.get(key)
    if db_value != False:
        networkDevicesDB.rem(key)
        return db_value, 200
    return {},200
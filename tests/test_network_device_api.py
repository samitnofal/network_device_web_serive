import requests
import json

def test_case_1_CRUD():
    # CRUD testing:
    for i in range(10):
        # Verify object not in DB
        api_url = f"http://127.0.0.1:5000/v1/network_devices/1.1.1.{i}"
        response = requests.get(api_url)
        assert response.status_code == 404, f"1.1.1.{i}"

        # Create object in DB 
        api_url = "http://127.0.0.1:5000/v1/network_devices"
        entry ={'fqdn':f"1.1.1.{i}", 'model':'ios-xr', 'version':'753'}
        response = requests.post(api_url, json=entry)
        assert response.status_code == 201,f"1.1.1.{i}"
        prev = response.json()

        # Get object in DB
        api_url = f"http://127.0.0.1:5000/v1/network_devices/1.1.1.{i}"
        response = requests.get(api_url)
        assert prev == response.json()
        assert response.status_code == 200,f"1.1.1.{i}"

        # Update object in DB change model
        api_url = f"http://127.0.0.1:5000/v1/network_devices/1.1.1.{i}"
        entry ={'model':'ios-xe', 'version':'753'}
        response = requests.put(api_url, json=entry)
        prev = response.json()
        assert response.status_code == 200,f"1.1.1.{i}"

        # Get object in DB
        api_url = f"http://127.0.0.1:5000/v1/network_devices/1.1.1.{i}"
        response = requests.get(api_url)
        assert response.status_code == 200,f"1.1.1.{i}"
        assert prev == response.json()

        # Update object in DB change version
        api_url = f"http://127.0.0.1:5000/v1/network_devices/1.1.1.{i}"
        entry ={'model':'ios-xe', 'version':'5555'}
        response = requests.put(api_url, json=entry)
        assert response.status_code == 200,f"1.1.1.{i}"
        prev = response.json()

        # Get object in DB
        api_url = f"http://127.0.0.1:5000/v1/network_devices/1.1.1.{i}"
        response = requests.get(api_url)
        assert response.status_code == 200,f"1.1.1.{i}"
        assert prev == response.json()

        # Delte object in DB
        api_url = f"http://127.0.0.1:5000/v1/network_devices/1.1.1.{i}"
        response = requests.delete(api_url)
        assert response.status_code == 200,f"1.1.1.{i}"

def test_case_2_test_list_function():
    # Get DB count
    api_url = f"http://127.0.0.1:5000/v1/network_devices"
    response = requests.get(api_url)
    assert response.status_code == 200
    prevous_cnt = len(response.json())

    for i in range(200):
        # Create object in DB 
        api_url = "http://127.0.0.1:5000/v1/network_devices"
        entry ={'fqdn':f"ed{i}", 'model':'ios-xr', 'version':'753'}
        response = requests.post(api_url, json=entry)
        assert response.status_code == 201
    
    # Get object in DB
    api_url = f"http://127.0.0.1:5000/v1/network_devices"
    response = requests.get(api_url)
    assert response.status_code == 200
    curr_cnt = len(response.json())
    assert prevous_cnt+200 == curr_cnt

    for i in range(200):
        # Delete object in DB 
        api_url = f"http://127.0.0.1:5000/v1/network_devices/ed{i}"
        response = requests.delete(api_url)
        assert response.status_code == 200

def test_case_3_test_error_cases():

    # Test invalid key
    api_url = f"http://127.0.0.1:5000/v1/network_devices/3733636636363636dedadedeafeafeafae"
    entry ={'model':'ios-xe', 'version':'753'}
    response = requests.put(api_url, json=entry)
    assert response.status_code == 400

    # Test invalid model
    api_url = f"http://127.0.0.1:5000/v1/network_devices/234242"
    entry ={'model':'XXXX', 'version':'753'}
    response = requests.put(api_url, json=entry)
    assert response.status_code == 400

    # Test invalid json data
    api_url = f"http://127.0.0.1:5000/v1/network_devices/234242"
    entry ={'model':'XXXX', 'version':'}}'}
    response = requests.put(api_url, json=entry)
    assert response.status_code == 400

    # Test invalid json data UPDATE
    api_url = f"http://127.0.0.1:5000/v1/network_devices/234242"
    entry = {}
    response = requests.put(api_url, json=entry)
    assert response.status_code == 400

    # Test invalid json data ADD
    api_url = f"http://127.0.0.1:5000/v1/network_devices"
    entry = {}
    response = requests.post(api_url, json=entry)
    assert response.status_code == 400

    # Test invalid No key given ADD
    api_url = f"http://127.0.0.1:5000/v1/network_devices"
    entry ={'model':'ios-xe', 'version':'753'}
    response = requests.post(api_url, json=entry)
    assert response.status_code == 400

    # Test invalid No key given DELETE
    api_url = f"http://127.0.0.1:5000/v1/network_devices"
    response = requests.delete(api_url)
    assert response.status_code == 405

def test_case_4_test_update():

    # Test update with Update object in DB change model
    api_url = f"http://127.0.0.1:5000/v1/network_devices/4.5.5.5"
    entry ={'model':'ios-xe', 'version':'753'}
    response = requests.put(api_url, json=entry)
    assert response.status_code == 201
    prev = response.json()

    api_url = f"http://127.0.0.1:5000/v1/network_devices/4.5.5.5"
    response = requests.delete(api_url)
    assert response.status_code == 200

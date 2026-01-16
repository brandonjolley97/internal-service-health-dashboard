
def test_maintenance_lock(client):

    # Create OFFLINE service
    res = client.post("/services", json={"name": "test-notifier", "description": "Sends test notifications", "status": "OFFLINE"})
    assert res.status_code == 201, res.text
    service_id = res.json()["id"]

    # Changing directly to ONLINE should fail
    res = client.put(f"/services/{service_id}/status", json={"status": "ONLINE"})
    assert res.status_code == 400, res.text

    # Changing to MAINTENANCE should succeed
    res = client.put(f"/services/{service_id}/status", json={"status": "MAINTENANCE"})
    assert res.status_code == 200, res.text
    assert res.json()["status"] == "MAINTENANCE"

    # Changing from MAINTENANCE to ONLINE should succeed
    res = client.put(f"/services/{service_id}/status", json={"status": "ONLINE"})
    assert res.status_code == 200, res.text
    assert res.json()["status"] == "ONLINE"



def test_degraded_requires_reason(client):

    # Create ONLINE service
    res = client.post("/services", json={"name": "test-notifier-2", "description": "Sends test notifications", "status": "ONLINE"})
    assert res.status_code == 201, res.text
    service_id = res.json()["id"]

    # Changing to DEGRADED without a reason should fail
    res = client.put(f"/services/{service_id}/status", json={"status": "DEGRADED"})
    assert res.status_code == 400, res.text

    # Changing to DEGRADED with reason only having spaces should fail
    res = client.put(f"/services/{service_id}/status", json={"status": "DEGRADED", "reason": "   "})
    assert res.status_code == 400, res.text

    # Changing to DEGRADED with reason having at least one character should succeed
    res = client.put(f"/services/{service_id}/status", json={"status": "DEGRADED", "reason": "Testing this status"})
    assert res.status_code == 200, res.text

    # The service status change should be saved
    assert res.json()["status"] == "DEGRADED"
    assert res.json()["degraded_reason"] == "Testing this status"



def test_service_name_conventions(client):

    # Creating a service with a name with spaces should fail
    res = client.post("/services", json={"name": "test-notifier 3", "description": "Has space in name", "status": "ONLINE"})
    assert res.status_code == 422, res.text

    # Creating a service with a name with '!' should fail
    res = client.post("/services", json={"name": "test-notifier!3", "description": "Has bad special character in name", "status": "ONLINE"})
    assert res.status_code == 422, res.text



def test_service_name_unique(client):
    
    # Creating a service with a unique name
    res = client.post("/services", json={"name": "test-notifier-4", "description": "Original service", "status": "ONLINE"})
    assert res.status_code == 201, res.text

    # Creating a service with the same name as an existing service should fail
    res = client.post("/services", json={"name": "test-notifier-4", "description": "Duplicate service", "status": "ONLINE"})
    assert res.status_code in (400,409), res.text
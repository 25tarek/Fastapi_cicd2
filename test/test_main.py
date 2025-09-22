from fastapi.testclient import TestClient
from src.main import api, tickets

client = TestClient(api)


def setup_function():
    tickets.clear()


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}


def test_add_ticket():
    ticket_data = {
        "id": 1,
        "flight_name": "AirBD",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Dhaka"
    }
    response = client.post("/ticket", json=ticket_data)
    assert response.status_code == 200
    assert response.json() == ticket_data


def test_get_tickets():
    client.post("/ticket", json={
        "id": 1,
        "flight_name": "AirBD",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Dhaka"
    })
    response = client.get("/ticket")
    assert response.status_code == 200
    tickets_list = response.json()
    assert isinstance(tickets_list, list)
    assert len(tickets_list) == 1
    assert tickets_list[0]["id"] == 1


def test_update_ticket():
    client.post("/ticket", json={
        "id": 1,
        "flight_name": "AirBD",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Dhaka"
    })
    updated_data = {
        "id": 1,
        "flight_name": "AirAsia",
        "flight_date": "2025-10-20",
        "flight_time": "16:00",
        "destination": "Chittagong"
    }
    response = client.put("/ticket/1", json=updated_data)
    assert response.status_code == 200
    assert response.json() == updated_data


def test_delete_ticket():
    client.post("/ticket", json={
        "id": 1,
        "flight_name": "AirBD",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "Dhaka"
    })
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    deleted_ticket = response.json()
    assert deleted_ticket["id"] == 1
    response_check = client.get("/ticket")
    assert response_check.json() == []


def test_delete_nonexistent_ticket():
    response = client.delete("/ticket/999")
    assert response.status_code == 200
    assert response.json() == {"error": "Ticket not found, deletion failed"}

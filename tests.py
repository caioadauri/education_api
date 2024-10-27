import pytest
import requests

BASE_URL = 'http://127.0.0.1:5000'
teacher = []

def test_create_teacher():
  new_teacher_data = {
    "name": "Caio",
    "age": "30",
    "matter": "Desenvolvimento de APIs",
    "obs": "Desenvolvento APIs"
  }
  response = requests.post(f"{BASE_URL}/teacher", json=new_teacher_data)
  assert response.status_code == 200
  response_json = response.json()
  assert "message" in response_json
  assert "id" in response_json
  teacher.append(response_json['id'])

def test_get_teachers():
  response = requests.get(f"{BASE_URL}/teacher")
  assert response.status_code == 200
  response_json = response.json()
  assert "teachers" in response_json
  assert "total_teacher" in response_json
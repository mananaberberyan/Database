import requests
from faker import Faker
import random
from datetime import date, timedelta

BASE_URL = 'http://127.0.0.1:8000'  
fake = Faker()

def create_equipment():
    url = f"{BASE_URL}/equipment/"
    data = {
        "equipment_name": fake.word(),
        "start_explotation": (date.today() - timedelta(days=random.randint(1, 365))),
        "term_explotation": (date.today() + timedelta(days=random.randint(1, 365))),
        "manufacturer": fake.company(),
    }
    response = requests.post(url, json=data)
    return response.json()

def create_material():
    url = f"{BASE_URL}/material/"
    data = {
        "material_name": fake.word(),
        "type": fake.word(),
        "price": round(random.uniform(1, 100), 2),
        "measurement": random.randint(1, 10),
        "alternativa": fake.word(),
    }
    response = requests.post(url, json=data)
    return response.json()

def create_product_specification():
    equipment_id = random.randint(1, 50)  
    material_id = random.randint(1, 50)  

    url = f"{BASE_URL}/product_specifications/"
    data = {
        "equipment_id": equipment_id,
        "material_id": material_id,
        "name": fake.word(),
        "duration": random.randint(1, 10),
    }
    response = requests.post(url, json=data)
    return response.json()

for _ in range(50):  
    create_equipment()

for _ in range(50):  
    create_material()

for _ in range(50):  
    create_product_specification()
    
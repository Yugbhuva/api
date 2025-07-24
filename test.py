import os
os.environ["ENVIRONMENT"] = "development"

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_basic():
    # Test root endpoint
    response = client.get("/")
    print(f"Root: {response.status_code} - {response.json()}")
    
    # Test health
    response = client.get("/health")
    print(f"Health: {response.status_code} - {response.json()}")
    
    # Test get items (should be empty initially)
    response = client.get("/api/v1/items/")
    print(f"Get Items: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    test_basic()
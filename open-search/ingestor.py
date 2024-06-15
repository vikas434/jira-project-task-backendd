import requests
import json
from datetime import datetime, timedelta
import random

# OpenSearch cluster URL and admin credentials
opensearch_url = "https://localhost:9200"
username = "admin"
password = "Ranjan@123"

# Index name
index_name = "projects"

# Function to generate random data for documents
def generate_sample_data(num_documents):
    data = []
    base_date = datetime(2024, 1, 1)
    for i in range(num_documents):
        start_date = base_date + timedelta(days=random.randint(0, 30))
        end_date = start_date + timedelta(days=random.randint(60, 365))
        budget_start_period = start_date
        budget_end_period = end_date
        actual_start_period = start_date
        actual_end_period = start_date + timedelta(days=random.randint(30, 180))

        document = {
            "project_id": str(i+1),
            "project_description": f"Sample project description {i+1}",
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "owner": f"Owner {i+1}",
            "status": random.choice(["ongoing", "completed", "not started"]),
            "budget_cost": {
                "start_period": budget_start_period.strftime("%Y-%m-%d"),
                "end_period": budget_end_period.strftime("%Y-%m-%d"),
                "value": round(random.uniform(10000, 100000), 2)
            },
            "actual_cost": {
                "start_period": actual_start_period.strftime("%Y-%m-%d"),
                "end_period": actual_end_period.strftime("%Y-%m-%d"),
                "value": round(random.uniform(5000, 50000), 2)
            },
            "location": random.choice(["New York", "San Francisco", "Boston", "Chicago"]),
            "risk_count": random.randint(1, 10),
            "risk_score": round(random.uniform(1, 10), 2),
            "task_count": random.randint(50, 200)
        }
        data.append(document)
    return data

# Function to test connection to OpenSearch
def test_connection():
    try:
        response = requests.get(opensearch_url, auth=(username, password), verify=False)
        if response.status_code == 200:
            print("Connection to OpenSearch successful.")
        else:
            print(f"Connection to OpenSearch failed with status code: {response.status_code}")
    except Exception as e:
        print(f"Error connecting to OpenSearch: {e}")

# Function to bulk ingest data in smaller chunks
def bulk_ingest(data, index_name, chunk_size=100):
    headers = {"Content-Type": "application/x-ndjson"}
    for i in range(0, len(data), chunk_size):
        bulk_data = ""
        chunk = data[i:i + chunk_size]
        for doc in chunk:
            bulk_data += json.dumps({"index": {"_index": index_name}}) + "\n"
            bulk_data += json.dumps(doc) + "\n"
        try:
            response = requests.post(f"{opensearch_url}/_bulk", headers=headers, data=bulk_data, auth=(username, password), verify=False, timeout=60)
            if response.status_code == 200 or response.status_code == 201:
                print(f"Successfully ingested chunk {i//chunk_size + 1}")
            else:
                print(f"Error ingesting chunk {i//chunk_size + 1}: {response.text}")
        except Exception as e:
            print(f"Error ingesting chunk {i//chunk_size + 1}: {e}")

# Test connection
test_connection()

# Generate 1000 sample documents
sample_data = generate_sample_data(1000)

# Ingest the sample data using bulk API
bulk_ingest(sample_data, index_name)

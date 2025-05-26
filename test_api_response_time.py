import requests
import time

url = "http://localhost:8001/predict"  # no trailing slash

headers = {"Content-Type": "application/json"}

queries = ["What is AI?", "How does machine learning work?"] * 25  # total 50

success_count = 0
total_time = 0

for i, query in enumerate(queries, 1):
    data = {"message": query}

    start = time.time()
    response = requests.post(url, json=data, headers=headers)
    elapsed = (time.time() - start) * 1000  # in ms
    total_time += elapsed

    if response.status_code == 200:
        print(f"Test {i} passed in {elapsed:.2f} ms")
        success_count += 1
    else:
        print(f"Test {i} failed with status {response.status_code}")

print(f"\n Total Successful Requests: {success_count}/50")
print(f" Average Response Time: {total_time/50:.2f} ms")

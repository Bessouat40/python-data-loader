import requests

def fetch_api_data(api_url, params):
    try:
        response = requests.post(api_url, json=params)
        if response.status_code == 200:
            print('ok')
        else:
            print(f"Error occured : {response.status_code}")
            return None
    except Exception as e:
        print(f"Error occured : {e}")
        return None

api_path = "http://localhost:8000/ingest"
params = {'path': "path_to_your_test_folder"}
data = fetch_api_data(api_path, params)
if data:
    print(data)
else:
    print("No data to display")

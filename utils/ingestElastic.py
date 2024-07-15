import requests

def fetch_api_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            print('ok')
        else:
            print(f"Error occured : {response.status_code}")
            return None
    except Exception as e:
        print(f"Error occured : {e}")
        return None

api_path = "http://localhost:8000/ingestElastic"
data = fetch_api_data(api_path)
print('done')

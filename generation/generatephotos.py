import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

def generate_image(prompt, image = "", size="1024*1024", strength=0.8):
  

    API_KEY = os.getenv("WAVESPEED_API_KEY")
    if not API_KEY:
        print("API key not found. Please check your environment variables.")
        return None

    url = "https://api.wavespeed.ai/api/v3/luma/photon-flash-modify"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    payload = {
        "enable_base64_output": False,
        "enable_safety_checker": True,
        "enable_sync_mode": False,
        "image": image,
        "num_images": 1,
        "output_format": "jpeg",
        "prompt": prompt,
        "seed": -1,
        "size": size,
        "strength": strength
    }

    begin = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        print(f"Error submitting task: {response.status_code}, {response.text}")
        return None

    request_id = response.json()["data"]["id"]
    print(f"Task submitted. Request ID: {request_id}")

    # Polling for result
    result_url = f"https://api.wavespeed.ai/api/v3/predictions/{request_id}/result"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    while True:
        response = requests.get(result_url, headers=headers)
        if response.status_code == 200:
            result = response.json()["data"]
            status = result["status"]

            if status == "completed":
                end = time.time()
                print(f"Task completed in {end - begin:.2f} seconds.")
                return result["outputs"][0]

            elif status == "failed":
                print(f"Task failed: {result.get('error')}")
                return None

            else:
                print(f"Task status: {status}... waiting")
        else:
            print(f"Error while polling: {response.status_code}, {response.text}")
            return None

        time.sleep(0.1)

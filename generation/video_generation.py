
import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()


class WaveSpeedError(Exception):
    """Custom exception for WaveSpeed API errors."""
    pass


def generate_video(image_url: str, prompt: str, duration: int = 5, seed: int = -1) -> dict:
   
    API_KEY = os.getenv("WAVESPEED_API_KEY")
    if not API_KEY:
        raise WaveSpeedError("API key not found in environment variables.")

    url = "https://api.wavespeed.ai/api/v3/bytedance/seedance-v1-lite-i2v-480p"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    payload = {
        "duration": duration,
        "image": image_url,
        "prompt": prompt,
        "seed": -1
    }

    begin = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(payload) , timeout=20)
    if response.status_code != 200:
        raise WaveSpeedError(f"Submission failed: {response.status_code} - {response.text}")

    result = response.json()["data"]
    request_id = result["id"]

    status_url = f"https://api.wavespeed.ai/api/v3/predictions/{request_id}/result"
    status_headers = {"Authorization": f"Bearer {API_KEY}"}

    while True:
        response = requests.get(status_url, headers=status_headers)
        if response.status_code != 200:
            raise WaveSpeedError(f"Status check failed: {response.status_code} - {response.text}")

        result = response.json()["data"]
        status = result["status"]

        if status == "completed":
            total_time = time.time() - begin
            output_url = result["outputs"][0]
            return output_url
        elif status == "failed":
            raise WaveSpeedError(f"Task failed: {result.get('error')}")


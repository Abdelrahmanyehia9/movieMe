import tempfile
import requests


def download_temp_video(url):
    response = requests.get(url, stream=True)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    for chunk in response.iter_content(chunk_size=8192):
        temp_file.write(chunk)
    temp_file.close()
    return temp_file.name  
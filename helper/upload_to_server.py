import cloudinary
import cloudinary.uploader
import os
from helper.delete_file import delete_file

cloudinary.config(
  cloud_name = "dwa40hbcj",       
  api_key = "799441233269692",            
  api_secret = "FfqZHAJQlMxHt7_bjgpWR3NcH_g",       
  secure = True
)
  
class UploadFailed(Exception): pass
def upload_video_to_cloudinary(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        result = cloudinary.uploader.upload_large(
            file_path,
            resource_type="video",
            chunk_size=6000000  
        )
        delete_file(file_path)
        return result.get("secure_url")
    except Exception:
        raise UploadFailed("failed to upload")


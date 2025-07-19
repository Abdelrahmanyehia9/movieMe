from concurrent.futures import ThreadPoolExecutor
from generation.generatephotos import generate_image
from generation.video_generation import generate_video

def image_video_pipline( image_description: str, photo : str  , prompt :str  , video_duration = 5 ):
    results = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            "image": executor.submit(generate_image, image_description , photo),
            "video": executor.submit(generate_video, photo , prompt , video_duration)
        }

        for key, future in futures.items():
            results[key] = future.result()

    return results["image"], results["video"]

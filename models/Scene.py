
class Scene:
    def __init__(self, scene_number: int, image_description: str, video_direction: str):
        self.scene_number = scene_number
        self.image_description = image_description
        self.video_direction = video_direction

    def __repr__(self):
        return (
            f"Scene {self.scene_number}:\n"
            f"Image Description: {self.image_description}\n"
            f"Video Direction: {self.video_direction}\n"
        )

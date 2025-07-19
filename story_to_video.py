from chat_bot.get_voice_over import generate_voiceover_from_scenes
from generation.generatephotos import generate_image
from helper.upload_to_server import upload_video_to_cloudinary
from models.Scene import Scene
from models.VideoData import GeneratedVideo
from helper.pipline import image_video_pipline
from chat_bot.storytoScene import convert_story_to_scenes
from generation.video_generation import generate_video
from video_editing import videoEditing
from voice.voice_over import voice_generator
import time
import traceback

def generate_video_from_story(story: str, voice_over: bool, voice_over_lang: str = "مصرى", voice_gender: str = "male"):
    try:
        start_time = time.time() 
        print("🔍 Converting story to scenes...")
        raw_scenes = convert_story_to_scenes(story)
        if isinstance(raw_scenes, dict) and raw_scenes.get("error"):
            raise ValueError(raw_scenes["error"])

        print("✅ Scenes extracted successfully.")
        scenes = [Scene(**scene) for scene in raw_scenes]

        print("🖼️ Generating image for scene 1...")
        scene_1 = next((s for s in scenes if s.scene_number == 1), None)
        scene_2 = next((s for s in scenes if s.scene_number == 2), None)
        scene_3 = next((s for s in scenes if s.scene_number == 3), None)

        if not scene_1 or not scene_2 or not scene_3:
            raise ValueError("Missing one or more required scenes (scene 1, 2, or 3).")

        first_scene_photo = generate_image(prompt=scene_1.image_description)
        print("✅ Scene 1 image generated.")

        print("🎞️ Generating video for scene 2...")
        second_scene_photo, first_scene_video = image_video_pipline(
            image_description=scene_2.image_description,
            photo=first_scene_photo,
            prompt=scene_1.video_direction
        )
        print("✅ Scene 2 video generated.")

        print("🎞️ Generating video for scene 3...")
        third_scene_photo, second_scene_video = image_video_pipline(
            image_description=scene_3.image_description,
            photo=second_scene_photo,
            prompt=scene_2.video_direction,
            video_duration=10
        )
        print("✅ Scene 3 video generated.")

        print("📽️ Generating final video for scene 3...")
        third_scene_video = generate_video(
            image_url=third_scene_photo,
            prompt=scene_3.video_direction
        )
        print("✅ Final video for scene 3 generated.")

        videos = [first_scene_video, second_scene_video, third_scene_video]

        voice = None
        voice_prompt = "No Voice Over"
        if voice_over:
            print("🗣️ Generating voiceover script...")
            voice_prompt = generate_voiceover_from_scenes(story=story, language_or_accent=voice_over_lang)
            print("✅ Voiceover script generated.")

            print("🎙️ Generating voiceover audio...")
            voice = voice_generator(voice_prompt, voice_gender)
            print("✅ Voiceover audio generated.")

        print("🧩 Combining videos and voiceover...")
        output_path = videoEditing(videos, voice)
        print(f"✅ Final video created: {output_path}")

        print("☁️ Uploading video to Cloudinary...")
        final_url = upload_video_to_cloudinary(output_path)
        print(f"✅ Video uploaded: {final_url}")

        duration = time.time() - start_time

        return GeneratedVideo(
            scenes=scenes,
            videoUrl=final_url,
            isVoiceOver=voice_over,
            photos=[first_scene_photo, second_scene_photo, third_scene_photo],
            voiceOverLang=voice_over_lang,
            duration=duration,
            status="completed",
            voiceOverText=voice_prompt,
            voiceOverGender=voice_gender
        )

    except Exception as e:
        print("❌ An error occurred during video generation:")
        traceback.print_exc()
        return {
            "error": f"Video generation failed: {str(e)}"
        }

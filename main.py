from flask import Flask, request, jsonify
from openai import OpenAI
from generation.generatephotos import generate_image
from story_to_video import generate_video_from_story
from story_to_video import generate_video_from_story
from chat_bot.storytoScene import convert_story_to_scenes
from generation.video_generation import WaveSpeedError, generate_video

app = Flask(__name__)
client = OpenAI()

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    story = data.get("story", "")

    result = convert_story_to_scenes(story)
    return jsonify(result=result)

@app.route("/generate_photo", methods=["POST"])
def image():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    result = generate_image(prompt)
    return jsonify(result)
@app.route("/generate-video", methods=["POST"])
def video():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        image = data.get("image", "").strip()

        if not prompt or not image:
            return jsonify({"error": "Both 'prompt' and 'image' fields are required."}), 400

        result = generate_video(image_url=image, prompt=prompt)
        return jsonify(result), 200

    except WaveSpeedError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Unexpected error occurred.", "details": str(e)}), 500
@app.route("/automatic-generation", methods=["POST"])
def auto_generate():
    try:
        data = request.get_json()

        story = data.get("story", "").strip()
        voice_over_enabled = data.get("is_voice_over", False)
        voice_over_gender = data.get("voice_over_gender", "").strip()
        lang = data.get("lang", "").strip()

        if not story:
            return jsonify({"error": "'story' field is required."}), 400

        generated_video = generate_video_from_story(
            story=story,
            voice_over=voice_over_enabled,
            voice_gender=voice_over_gender,
            voice_over_lang=lang
        )

        # تحويل كائن GeneratedVideo إلى dict لسهولة الإرجاع في JSON
        response = {
            "url": generated_video.videoUrl,
            "duration": round(generated_video.duration, 2),
            "status": generated_video.status,
            "is_voice_over": generated_video.isVoiceOver,
            "voice_over_lang": generated_video.voiceOverLang,
            "voice_over_gender": generated_video.voiceOverGender,
            "voice_over_text": generated_video.voiceOverText,
            "photos": generated_video.photos,
            "scenes": [scene.__dict__ for scene in generated_video.scenes],
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": "Unexpected error occurred.", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
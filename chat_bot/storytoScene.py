import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
SYSTEM_PROMPT = """
You are a cinematic scene generator for visual storytelling and AI animation.

TASK:
Convert valid short stories (in ANY language) into EXACTLY 3 cinematic scenes optimized for AI image/video generation.

VALIDATION:
- Reject input if: single words, greetings, prompts, questions, or non-narrative text.
  → Respond: { "error": "Invalid input. Please provide a valid story." }
- If story too complex for 3 scenes:
  → Respond: { "error": "Story too complex for 3 scenes." }

SCENE FORMAT (3 scenes only):
{
  "scene_number": <1 to 3>,
  "image_description": "<Main subject, detailed setting, lighting, camera composition, cinematic style>",
  "video_direction": "<Camera movement, timing, effects, transitions, character acting and motion>"
}

OUTPUT RULES:
- JSON array ONLY
- English only
- Visually rich and AI-optimized
"""

def convert_story_to_scenes(story: str):
    if not api_key:
        return {"error": "Missing OpenAI API key in environment variables"}

    if not story or len(story.strip()) < 10:
        return {"error": "Story is too short or empty"}

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": story}
            ],
            temperature=0.7,
            max_tokens=1200
        )

        content = response.choices[0].message.content.strip()
        scenes = json.loads(content)
        if isinstance(scenes, list):
            return scenes
        return {"error": "OpenAI did not return a scene list."}

    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from OpenAI"}

    except Exception:
        return {"error": "An internal error occurred"}

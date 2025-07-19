import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

VOICEOVER_SYSTEM_PROMPT = """
You are an expert cinematic voice-over scriptwriter for animated scenes.

Analyze the visual scenes for: emotional tone, key elements, and pacing needs.

Write a natural, cinematic voice-over narration that:
- Creates immersive story experience
- Uses vivid, emotional language
- Builds tension/excitement as needed
- Matches specified language/accent
- Duration: 25-30 seconds (80-120 words)
- Include natural pauses with "..."
- Structure: Hook → Build → Impact

Output ONLY clean narration text with pause markers.
No formatting, explanations, or stage directions.

If scenes unclear: { "error": "Scenes require clearer visual description." }

Tone examples:
- Action: Short, urgent sentences
- Romance: Flowing, warm language
- Mystery: Whispered intensity with pauses
- Adventure: Bold, inspiring energy
"""

def generate_voiceover_from_scenes(story: str, language_or_accent: str = "مصرى") -> dict:
    if not api_key:
        return {"error": "Missing OpenAI API key in environment variables"}
    
    if not story:
        return {"error": "story must be a non-empty"}

   

    user_prompt = f"""
Language or accent: {language_or_accent}

story:
{story}

Please write a short voice-over narration based on these story.
"""

    response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": VOICEOVER_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.85,
            max_tokens=300
        )

    content = response.choices[0].message.content.strip()

    if content.startswith("{") and "error" in content:
            return json.loads(content)

    return  content

  

  
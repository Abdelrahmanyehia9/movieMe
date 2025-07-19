import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
import moviepy.video.fx.all as vfx
from helper.download_temp_video import download_temp_video

def videoEditing(video_urls, voiceover_path=None, output_path="final_output.mp4", fade_duration=0.5):
    temp_video_files = []

    try:
        for url in video_urls:
            path = download_temp_video(url)
            temp_video_files.append(path)

        clips = []
        for path in temp_video_files:
            clip = VideoFileClip(path)

            clip = vfx.speedx(clip, 0.7)

            clip = clip.fadein(fade_duration).fadeout(fade_duration)

            clips.append(clip)

        final_clip = concatenate_videoclips(clips, method="compose")

        if voiceover_path:
            audio = AudioFileClip(voiceover_path)
            if audio.duration >= final_clip.duration:
                audio = audio.set_duration(final_clip.duration)
            final_clip = final_clip.set_audio(audio)

        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
        return output_path

    finally:
        for path in temp_video_files:
            try:
                os.remove(path)
            except Exception:
                pass

# video_enhancer.py

from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, VideoFileClip
from moviepy.video.tools.subtitles import SubtitlesClip
from gtts import gTTS
from datetime import timedelta
import os

# Constants
FONT = "Arial"
FONT_SIZE = 36
FONT_COLOR = "white"
BG_COLOR = "black"
BGM_PATH = "default_bgm.mp3"  # bundled with your repo

def generate_srt_from_text(text, output_srt_path, duration_per_line=4):
    """Generate .srt subtitles file from multi-line text."""
    lines = text.strip().split("\n")
    with open(output_srt_path, "w", encoding="utf-8") as f:
        for i, line in enumerate(lines):
            start_time = timedelta(seconds=i * duration_per_line)
            end_time = timedelta(seconds=(i + 1) * duration_per_line)
            f.write(f"{i+1}\n")
            f.write(f"{str(start_time)[:-3].replace('.', ',')} --> {str(end_time)[:-3].replace('.', ',')}\n")
            f.write(f"{line}\n\n")

def create_subtitle_clips_from_srt(srt_path):
    """Convert .srt to a SubtitlesClip usable in moviepy."""
    generator = lambda txt: TextClip(txt, font=FONT, fontsize=FONT_SIZE, color=FONT_COLOR, bg_color=BG_COLOR)
    return SubtitlesClip(srt_path, generator)

def enhance_video_with_subtitles_and_bgm(input_video_path, output_video_path, srt_path, bgm_path=BGM_PATH):
    video = VideoFileClip(input_video_path)
    subs = create_subtitle_clips_from_srt(srt_path)
    video = CompositeVideoClip([video, subs.set_position(('center','bottom'))])

    if os.path.exists(bgm_path):
        bgm = AudioFileClip(bgm_path).volumex(0.2)
        bgm = bgm.set_duration(video.duration)
        video = video.set_audio(bgm)

    video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")

# Example usage:
# text = """Hello there\nThis is an AI-generated video\nThank you for watching"""
# generate_srt_from_text(text, "output.srt")
# enhance_video_with_subtitles_and_bgm("input.mp4", "final_output.mp4", "output.srt")

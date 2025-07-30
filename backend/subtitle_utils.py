from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
import srt
from datetime import timedelta
import os


def export_srt(text, duration=10, words_per_caption=6, output_path="output.srt"):
    """
    Converts text into SRT subtitles and saves to output_path.
    """
    lines = []
    words = text.split()
    start = 0
    index = 1
    while start < len(words):
        end = start + words_per_caption
        chunk = words[start:end]
        content = " ".join(chunk)
        start_time = timedelta(seconds=(index - 1) * duration)
        end_time = timedelta(seconds=index * duration)
        sub = srt.Subtitle(index=index, start=start_time, end=end_time, content=content)
        lines.append(sub)
        start += words_per_caption
        index += 1

    srt_data = srt.compose(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_data)
    return output_path


def add_subtitles_and_bgm(
    video_path,
    srt_path,
    bgm_path,
    output_path="enhanced_output.mp4",
    font="Arial-Bold",
    font_size=36,
    font_color="white",
    subtitle_position=("center", "bottom")
):
    """
    Adds subtitles from .srt and background music to the given video.
    """
    # Load video
    video = VideoFileClip(video_path)

    # Parse .srt file
    with open(srt_path, "r", encoding="utf-8") as f:
        subtitles = list(srt.parse(f.read()))

    # Create subtitle clips
    def make_textclip(txt):
        return TextClip(txt, font=font, fontsize=font_size, color=font_color, stroke_color='black', stroke_width=2)

    subtitle_clips = []
    for sub in subtitles:
        txt_clip = (make_textclip(sub.content)
                    .set_position(subtitle_position)
                    .set_start(sub.start.total_seconds())
                    .set_duration((sub.end - sub.start).total_seconds()))
        subtitle_clips.append(txt_clip)

    # Background music
    if os.path.exists(bgm_path):
        bgm = AudioFileClip(bgm_path).volumex(0.2)  # reduce volume
        bgm = bgm.set_duration(video.duration)
        final_audio = video.audio.volumex(0.8).audio_fadein(1).audio_fadeout(1).set_duration(video.duration)
        final_audio = final_audio.set_audio(bgm)
    else:
        final_audio = video.audio

    final = CompositeVideoClip([video, *subtitle_clips])
    final = final.set_audio(final_audio)

    # Export final video
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=video.fps)
    return output_path


# Aliases for compatibility with streamlit_ui.py
generate_srt_from_text = export_srt
enhance_video_with_subtitles_and_bgm = add_subtitles_and_bgm

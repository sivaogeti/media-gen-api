from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_audioclips
import os
from typing import List, Tuple


def export_srt(transcript: List[str], duration: float, output_path: str):
    """
    Exports transcript as a .srt subtitle file assuming equal spacing.
    """
    lines = []
    segment_duration = duration / len(transcript)
    
    for idx, line in enumerate(transcript):
        start_time = segment_duration * idx
        end_time = segment_duration * (idx + 1)

        def format_time(t):
            h = int(t // 3600)
            m = int((t % 3600) // 60)
            s = int(t % 60)
            ms = int((t % 1) * 1000)
            return f"{h:02}:{m:02}:{s:02},{ms:03}"

        lines.append(f"{idx+1}")
        lines.append(f"{format_time(start_time)} --> {format_time(end_time)}")
        lines.append(line.strip())
        lines.append("")  # Empty line for spacing

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def add_subtitles_and_bgm(
    video_path: str,
    transcript: List[str],
    output_path: str = "final_output.mp4",
    bgm_path: str = None,
    subtitle_font: str = "Arial",
    subtitle_size: int = 24,
    subtitle_color: str = "white",
    subtitle_position: Tuple[int, int] = ("center", "bottom")
):
    """
    Adds subtitles and optional background music to a video.
    """

    clip = VideoFileClip(video_path)
    duration = clip.duration
    segment_duration = duration / len(transcript)
    subtitle_clips = []

    for i, line in enumerate(transcript):
        txt = TextClip(
            line,
            fontsize=subtitle_size,
            font=subtitle_font,
            color=subtitle_color,
            method='caption',
            size=(clip.w * 0.8, None)  # 80% width
        ).set_position(subtitle_position).set_duration(segment_duration).set_start(i * segment_duration)

        subtitle_clips.append(txt)

    final_video = CompositeVideoClip([clip, *subtitle_clips])

    if bgm_path and os.path.exists(bgm_path):
        bgm = AudioFileClip(bgm_path).volumex(0.2).set_duration(duration)
        original_audio = clip.audio
        if original_audio:
            mixed_audio = original_audio.volumex(1.0).audio_fadein(0.5).audio_fadeout(0.5)
            final_audio = CompositeVideoClip([mixed_audio.set_start(0), bgm.set_start(0)]).audio
        else:
            final_audio = bgm
        final_video = final_video.set_audio(final_audio)

    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")


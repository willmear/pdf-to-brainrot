import os
from pathlib import Path

from dotenv import load_dotenv
import assemblyai as aai
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, CompositeVideoClip
from moviepy.video.fx.Crop import Crop
from termcolor import colored
# from moviepy.editor import *
# import moviepy.video.fx.all as vfx
from moviepy.video.fx.MultiplySpeed import MultiplySpeed
import random


load_dotenv('../.env')
aai.settings.api_key = os.getenv('ASSEMBLYAI_API_KEY')

FILE_URL = Path(__file__).parent / "audio" / "speech.mp3"
font_path = Path(__file__).parent / "theboldfont.ttf"
background_videos = Path(__file__).parent / "BACKGROUNDVIDEOS" / "minecraft.mp4"


def create_video(title, i):
    words = transcribe()
    gameplay = cut_video(words[-1].end)
    gameplay = add_audio(gameplay)
    gameplay = subtitle(gameplay, words)
    # gameplay = gameplay.fx(vfx.speedx, 1.25)
    # gameplay = MultiplySpeed(1.25).apply(gameplay)
    final_clip = CompositeVideoClip([gameplay])
    final_clip.write_videofile(f'C:\\videos\\{i}{title}.mp4', codec='libx264', audio_codec='aac', bitrate="5000k")


def transcribe():
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL.absolute().as_posix())
    if transcript.status == aai.TranscriptStatus.error:
        print(colored(transcript.error))
    else:
        print(colored("transcribed", 'green'))
        return transcript.words


def cut_video(length: int):
    # options = ["gta", "satisfying", "minecraft"]
    # choice = options[random.randint(0, 2)]
    # print(colored(choice, 'green'))
    # gameplay = VideoFileClip(f"C:\\BACKGROUNDVIDEOS\\{choice}.mp4")
    gameplay = VideoFileClip(background_videos.absolute().as_posix())
    gameplay = gameplay.without_audio()

    (w, h) = gameplay.size
    Crop(width=600, height=5000, x_center=w / 2, y_center=h / 2).apply(gameplay)

    start_time = random.uniform(0, gameplay.duration-(length / 1000)-2)
    end_time = start_time + (length / 1000) + 2

    return gameplay.subclipped(start_time, end_time)


def add_audio(gameplay: VideoFileClip):
    audio_clip = AudioFileClip(FILE_URL)
    new_audio_clip = CompositeAudioClip([audio_clip])
    gameplay.audio = new_audio_clip
    return gameplay


def subtitle(gameplay: VideoFileClip, words):
    clip_list = [gameplay]

    objects = three_per_line(words)

    for word_group in objects:

        text = ' '.join(word.text for word in word_group)
        print(colored(text, "blue"))

        duration = word_group[-1].end - word_group[0].start

        txt_clip = (TextClip(text=text, font_size=50, color='white', font=font_path.absolute().as_posix(),
                             size=(gameplay.w, gameplay.h), method="caption",
                             stroke_width=2, stroke_color="black")
                    .with_position(('center', 'center'))
                    .with_duration(duration / 1000)
                    .with_start(t=word_group[0].start / 1000))

        clip_list.append(txt_clip)

    final_clip = CompositeVideoClip(clip_list)
    return final_clip


def three_per_line(words):
    for i in range(0, len(words), 3):
        yield words[i:i + 3]
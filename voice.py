import os
import sys
import tempfile
import time
import uuid
from fakeyou import FakeYou
from matplotlib import path
import requests
from pydub import AudioSegment

# Kanye artist_token = "TM:1a7mjjxwq4js"
# Snoop artist_token = "TM:hqcecn351tpc"
# Biggi artist_token = "TM:0ys5r1ywkx5j"

fakeyou = FakeYou()

def get_track(lyrics_path: str, artist_token: str):
    output_folder = tempfile.gettempdir() + "\\finished_music"
    output_path = f"{output_folder}\\rap_{artist_token}_{uuid.uuid4()}.mp3"

    rap: AudioSegment = get_rap(lyrics_path=lyrics_path, artist_token=artist_token)
    rap.export(output_path)
    return output_path

def get_rap(lyrics_path: str, artist_token: str):
    rap_segments = get_rap_segments(lyrics_path=lyrics_path, artist_token=artist_token)
    rap = AudioSegment.empty()
    for i in range(0, len(rap_segments)):
        rap += rap_segments[i][0:rap_segments[i].__len__()-500]
    return rap

def get_rap_segments(lyrics_path: str, artist_token: str):
    job_tokens = []
    text_segments = get_text_segments(lyrics_path=lyrics_path)
    for text_segment in text_segments:
        while True:
            try:
                print("Job request made")
                job_token = fakeyou.make_tts_job(text=text_segment, ttsModelToken=artist_token)
                job_tokens.append(job_token)
                print("Job request successful")
                break
            except:
                print("Job request failed")
                time.sleep(5)

    jobs = []
    for job_token in job_tokens:
        job = fakeyou.tts_poll(job_token)
        jobs.append(job)
        print("Job detected")

    audio_segments = []
    for job in jobs:
        response = requests.get(job.link)
        split = response.url.split("/")
        filename = "raw\\" + split[split.__len__() - 1]
        with open(filename, "wb") as f:
            f.write(response.content)
        audio_segment = AudioSegment.from_file(filename)
        audio_segments.append(audio_segment)
        print("Job downloaded")

    return audio_segments

def get_text_segments(lyrics_path: str):
    text_split = []
    with open(lyrics_path, "r") as f:
        text_split = f.readlines()  
    text_segments = []
    current_text = ""
    for line in text_split:
        if line == "\n":
            text_segments.append(current_text)
            current_text = ""
        else:
            current_text += line.replace("\n", "")
    text_segments.append(current_text)
    return text_segments

def ensure_output_dir_exists():
    output_folder = tempfile.gettempdir() + "\\finished_music"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

def main():
    ensure_output_dir_exists()

    args = sys.argv

    model_token = args[1]
    #model_token = "TM1a7mjjxwq4js"
    text_path = args[2]
    #text_path = "C:\\Users\\Schneider David\\Documents\\text.txt"

    os.system('cls' if os.name == 'nt' else 'clear')

    get_track(lyrics_path=text_path, artist_token=model_token)
    print("success")

if __name__ == "__main__":
    main()
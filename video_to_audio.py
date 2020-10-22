import subprocess
import argparse
import os
import time

parser = argparse.ArgumentParser(description='video_to_wav')
parser.add_argument('video_path', help='Path to video file')


class video_to_audio:

    def __init__(self, output):
        self.output = output

    def video_to_wav(self, video_path):
        wavs_path = "WAVs"
        name = video_path.split('/')[-1].split('.')[0]
        self.output = wavs_path + "/" + name + ".wav"
        if not os.path.exists(wavs_path):
            os.mkdir(wavs_path)
            print(f"Directory created")

        subprocess.run(["ffmpeg",
                "-loglevel",
                "debug",
                "-hide_banner",
                "-y",
                "-i",
                video_path,
                "-vn",
                "-sn",
                "-ar",
                "44100",
                "-q:a",
                "0",
                "-map",
                "a",
                self.output],
               stderr=subprocess.DEVNULL,
               stdout=subprocess.DEVNULL,
               stdin=subprocess.PIPE)

        print(f"Convertation to .wav finished!")


#if __name__ == '__main__':
    #path = "files/videoplayback.mp4"
    #video_to_wav(path)
    #args = parser.parse_args()
    #video_to_wav(args.video_path)


    def video2mp3(self, video_path):
        mp3s_path = "mp3s"
        name = video_path.split('/')[-1].split('.')[0]
        self.output = mp3s_path + "/" + name + ".mp3"
        if not os.path.exists(mp3s_path):
            os.mkdir(mp3s_path)
            print(f"Directory created")

        subprocess.run(["ffmpeg",
                "-loglevel",
                "debug",
                "-hide_banner",
                "-y",
                "-i",
                video_path,
                "-write_id3v1",
                "1",
                "-id3v2_version",
                "3",
                "-q:a",
                "0",
                "-map",
                "a",
                self.output],
               stderr=subprocess.DEVNULL,
               stdout=subprocess.DEVNULL,
               stdin=subprocess.PIPE)

        print(f"Convertation to .mp3 finished!")

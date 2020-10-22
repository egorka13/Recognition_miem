import subprocess
import argparse
import os

parser = argparse.ArgumentParser(description='mp3_to_wav')
parser.add_argument('in_mp3', help='Input .mp3 file')

def mp3_to_wav(mp3_path):
    wavs_path = "WAVs"
    wav_path = wavs_path + "/output.wav"
    if not os.path.exists(wavs_path):
        os.mkdir(wavs_path)

    subprocess.run(["ffmpeg",
                "-loglevel",
                "quiet",
                "-hide_banner",
                "-y",
                "-i",
                mp3_path,
                "-write_id3v1",
                "1",
                "-id3v2_version",
                "3",
                "-q:a",
                "0",
                "-map",
                "a",
                wav_path],
               stderr=subprocess.DEVNULL,
               stdout=subprocess.DEVNULL,
               stdin=subprocess.PIPE)


if __name__ == '__main__':
    args = parser.parse_args()
    mp3_to_wav(args.in_mp3)
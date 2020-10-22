import subprocess
import argparse
import os

parser = argparse.ArgumentParser(description='video2mp3')
parser.add_argument('video_path', help='Path to video file')


def video2mp3(video_path):
    mp3s_path = "mp3s"
    mp3_path = mp3s_path + "/output.mp3"
    if not os.path.exists(mp3s_path):
        os.mkdir(mp3s_path)

    subprocess.run(["ffmpeg",
                "-loglevel",
                "quiet",
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
                mp3_path],
               stderr=subprocess.DEVNULL,
               stdout=subprocess.DEVNULL,
               stdin=subprocess.PIPE)


if __name__ == '__main__':
    #path = "files/videoplayback.mp4"
    #video2mp3(path)
    args = parser.parse_args()
    video2mp3(args.video_path)

# -*- coding: utf-8 -*-

from test import Hello
import argparse
import sys
import socket
from TextFromPicture import Pic2Txt
import FFMPEGFrames
import glob
from SpeechRecognition import wav_to_txt
import video_to_audio
from import_to_db import text_to_db
from import_to_db import audio_to_db
from import_to_db import image_to_db
from import_to_db import video_to_db
import sqlite3


def main():
    parser = argparse.ArgumentParser()

    error_msg = "Invalid Arguments\n\n" \
                "Commands: \n" \
                "  -t, --test                 Let's test it!\n" \
                "       Optional: --name='your_arg'  -   that'll print your string your_arg\n" \
                "  -vi, --video             Convert video to pictures and then convert to text\n" \
                "       Mandatory: --in_filename='files/video.mp4' --out_filename='output.txt'  --fps='1'\n" \
                "       - set input video, output file, frames per second\n"\
                "  -va, --vaudio             Convert video to audio and then convert to text\n" \
                "       Mandatory: --in_filename='files/video.mp4' --out_filename='output.txt'\n"\
                "       - set input video and output file\n"\
                "  -a, --audio             Convert audio to text\n" \
                "       Mandatory: --in_filename='files/video.wav' --out_filename='output.txt'\n" \
                "       - set input audiofile and output file\n"\
                "  -i, --image             Convert pictures to text\n" \
                "       Mandatory: --in_filename='files' --out_filename='output.txt'\n" \
                "       - set input directory and output file"


    if len(sys.argv) == 1:
        print(error_msg)

    elif str(sys.argv[1]) in ['-t', '--test']:
        parser.add_argument('-t', '--test', action='store_true')
        parser.add_argument("--name", default=socket.gethostname())

        args = parser.parse_args()

        test_class = Hello(args.name)
        test_class.print_hello()
    elif str(sys.argv[1]) in ['-vi', '--video']:
        parser.add_argument('-vi', '--video', action='store_true')
        parser.add_argument("in_filename", help='Input filename')
        parser.add_argument('out_filename', help='Output filename')
        parser.add_argument("fps", help='fps')
        args = vars(parser.parse_args())

        input = args["in_filename"]
        output = args["out_filename"]
        fps = args["fps"]

        f = FFMPEGFrames.FFMPEGFrames("images/")
        f.extract_frames(input, fps)


        conn = sqlite3.connect("SaTRdatabase.db")
        cursor = conn.cursor()
        video_to_db(input, cursor)
        image_to_db(f.output, input, cursor)

        Pic2Txt(glob.glob(f.output + "/*.png"), output, cursor)

        conn.commit()
        conn.close()
    elif str(sys.argv[1]) in ['-va', '--vaudio']:
        parser.add_argument('-va', '--vaudio', action='store_true')
        parser.add_argument("in_filename", help='Input filename')
        parser.add_argument('out_filename', help='Output filename')
        args = vars(parser.parse_args())

        input = args["in_filename"]
        output = args["out_filename"]


        f = video_to_audio.video_to_audio("/WAVs")
        f.video_to_wav(input)

        conn = sqlite3.connect("SaTRdatabase.db")
        cursor = conn.cursor()
        video_to_db(input, cursor)
        audio_to_db(f.output, input, cursor)

        wav_to_txt(f.output, output, cursor)

        conn.commit()
        conn.close()
    elif str(sys.argv[1]) in ['-a', '--audio']:
        parser.add_argument('-a', '--audio', action='store_true')
        parser.add_argument("in_filename", help='Input filename')
        parser.add_argument('out_filename', help='Output filename')
        args = vars(parser.parse_args())

        input = args["in_filename"]
        output = args["out_filename"]

        conn = sqlite3.connect("SaTRdatabase.db")
        cursor = conn.cursor()
        vsourse = 'no_video'
        audio_to_db(input, vsourse, cursor)

        wav_to_txt(input, output, cursor)

        conn.commit()
        conn.close()
    elif str(sys.argv[1]) in ['-i', '--image']:
        parser.add_argument('-i', '--image', action='store_true')
        parser.add_argument("in_directory", help='Input directory')
        parser.add_argument('out_filename', help='Output filename')
        args = vars(parser.parse_args())

        input = args["in_directory"]
        output = args["out_filename"]

        conn = sqlite3.connect("SaTRdatabase.db")
        cursor = conn.cursor()
        vsourse = 'no_video'
        image_to_db(input, vsourse, cursor)

        Pic2Txt(glob.glob(input + "/*.png"), output, cursor)

        conn.commit()
        conn.close()
    else:
        print(error_msg)


if __name__ == '__main__':
    main()

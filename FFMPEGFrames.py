import os
import subprocess


class FFMPEGFrames:

    def __init__(self, output):
        self.output = output

    def extract_frames(self, input, fps):
        self.output = input.split('/')[-1].split('.')[0]

        if not os.path.exists(self.output):
            os.makedirs(self.output)

        query = "ffmpeg -i " + input + " -vf fps=" + \
            str(fps) + " " + self.output + "/output%02d.png"
        response = subprocess.Popen(
            query, shell=True, stdout=subprocess.PIPE).stdout.read()
        s = str(response).encode('utf-8')

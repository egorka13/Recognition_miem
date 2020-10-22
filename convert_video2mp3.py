'''конвертация видеофайлов различных форматов в mp3'''

import os
import sys
import subprocess
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
import time
import datetime

def videotomp3(task):
    '''запускает новый подпроцесс ffmpeg, используя pipe и сохраняет файлы в формате mp3 в ту жу директорию, где хранятся оригинальные файлы '''
    root_path = task[0]
    filename = task[1]
    full_path = os.path.join(root_path, filename)
    new_filename = os.path.splitext(filename)[0] +".mp3"
    new_path = os.path.join(root_path,
                            os.path.basename(root_path) + "-" + FOLDER_NAME,
                            new_filename)

    completed = subprocess.run(["ffmpeg",
                                "-loglevel",
                                "quiet",
                                "-hide_banner",
                                "-y",
                                "-i",
                                full_path,
                                "-write_id3v1",
                                "1",
                                "-id3v2_version",
                                "3",
                                "-q:a",
                                "0",
                                "-map",
                                "a",
                                new_path],
                               stderr=subprocess.DEVNULL,
                               stdout=subprocess.DEVNULL,
                               stdin=subprocess.PIPE)
    #Если не предоставить pipe каналу stdin, то ffmpeg не закроется корректно
    #при конвертировании нескольких файлов и будет необходимо перезагрузить
    #терминал после авершения выполнения этого скрипта
    #удалить исходные файлы после их конвертации
    #if completed.returncode == 0:
        #subprocess.call(["rm", full_path]) # удаляет исходный файл после конвертации
    print(f"'{new_path}' - return code {completed.returncode}")
    if completed.returncode != 0:
        completed.timestamp = datetime.datetime.now().ctime()
    return completed

if __name__ == "__main__":
    FOLDERS = []
    FOLDER_NAME = "MP3s"
    AUDIO_FILE_TYPES = ("webm",
                        "mpeg",
                        "ogg",
                        "mp4",
                        "m4p",
                        "m4v",
                        "avi",
                        "wmv",
                        "mov",
                        "flv")
    STARTTIME = time.time()
    #get all of the source audio filenames
    for root, dirs, files in os.walk(os.getcwd()):
        source_audio_filenames = []
        for file in files:
            if file.endswith(AUDIO_FILE_TYPES):
                source_audio_filenames.append((root, file))
        FOLDERS.append((root, source_audio_filenames))

    with ThreadPool(cpu_count())as p:
        PROCESSES = []
        for Folder in FOLDERS:
            try:
                #Stop directories being created within the output directories
                if FOLDER_NAME in Folder[0]:
                    continue
                NewFolderName = os.path.basename(Folder[0]) + "-" + FOLDER_NAME
                os.mkdir(os.path.join(Folder[0], NewFolderName))
            except FileExistsError:
                pass
            PROCESSES += Folder[1]
        print(f"Transcoding {len(PROCESSES)} Audio files")
        JOBS = p.map(videotomp3, PROCESSES)
        FAILED_JOBS = []
        for job in JOBS:
            if job.returncode != 0:
                FAILED_JOBS.append(job)
        MESSAGE = (f"Transcode Finished! \r {len(PROCESSES)-len(FAILED_JOBS)}/{len(PROCESSES)} "
                   f"Audio files transcoded in \r{time.time() - STARTTIME:.4f} seconds")
        subprocess.run(["notify-send", "--urgency=low", MESSAGE])
        if len(FAILED_JOBS) > 0:       
            with open("nautilus-transcode.log", 'a+') as f:
                for failedJob in FAILED_JOBS:
                    f.write(f"{failedJob.timestamp} args:{failedJob.args}"
                            f"return code:{failedJob.returncode}\n")

    print("Done")
    sys.exit(0)



# coding: utf-8

# ### Функции пред- и постобработки

# In[1]:


from pydub import AudioSegment
from scipy.io import wavfile
import os
import numpy as np
import speech_recognition as sr
import argparse
from import_to_db import text_to_db


parser = argparse.ArgumentParser(description="wav_to_txt")
parser.add_argument("wav_path", help="Path to .wav audio file")
parser.add_argument("out_path", help="Path to output .txt file")

# Делим аудио (wav) на короткие части, сохраняем в папку tmp_slices

# In[2]:




def divide_audio(audio_src, slice_length_ms=3000, overlap_ms=500):
    audio = AudioSegment.from_file(audio_src, "wav")

    slices = np.arange(0, len(audio) - overlap_ms, slice_length_ms - overlap_ms)

    path = "tmp_slices"
    os.mkdir(path)
    audio_slices_src = []
    i = 0

    for start, end in zip(slices[:-1], slices[1:]):
        slice_ = audio[start : end + overlap_ms]
        # сохраняем кусочки аудио
        slice_name = "tmp_slices\slice{0}.wav".format(i)
        audio_slices_src.append(slice_name)
        slice_.export(slice_name, format="wav")
        i += 1

    if len(audio) - end > overlap_ms:
        slice_ = audio[end: len(audio)]
        slice_name = "tmp_slices\slice{0}.wav".format(i)
        audio_slices_src.append(slice_name)
        slice_.export(slice_name, format="wav")

    return audio_slices_src


# Удаляем папку tmp_slices с частями аудио

# In[3]:


def delete_tmp_slices(audio_slices_src):
    for slice_ in audio_slices_src:
        os.remove(slice_)
    os.rmdir("tmp_slices")


# Соединяем распознанный по частям текст

# In[4]:


def combine_text(text_array):
    result_text = ""

    prev_splited = []

    for text in text_array:
        processed_text = ""

        splited = text.lower().split()

        j = 0
        while j < min(len(splited), len(prev_splited)):
            if splited[j] != prev_splited[-1 - j]:
                break
            j += 1

        for i in range(j, len(splited)):
            processed_text += splited[i] + " "

        result_text += processed_text

        prev_splited = splited

    return result_text


# ### Распознавание речи

# Библиотека SpeechRecognition ( https://pypi.org/project/SpeechRecognition/ )
#
# Используется распознавание при помощи Google Speech Recognition
#
# Распознавание текста происходит непрерывно, даже когда речи нет, а есть только шум. Если распознать какие-то слова не удается, программа выдает ошибку. Поэтому нужно делить аудио на короткие части и распознавать их отдельно.
#
# Список языковых кодов для Google Speech Recognition: https://www.science.co.il/language/Locale-codes.php

# In[5]:


# Распознавание без учета шума

# In[6]:


def recognize_no_noise(audio_src):
    r = sr.Recognizer()

    # делим аудио на части
    chunks_src = divide_audio(audio_src)
    # распознаем каждую часть
    text_array = []
    for chunk_src in chunks_src:
        a = sr.AudioFile(chunk_src)
        # print('analyzing ', chunk_src)
        with a as source:
            audio = r.record(source)
        try:
            text_chunk = r.recognize_google(audio, language="ru")
            text_array.append(text_chunk)
            # print('!',text_chunk)
        except:
            pass
    # объединяем распознанные тексты
    text = combine_text(text_array)

    # удаляем ненужные файлы
    delete_tmp_slices(chunks_src)

    return text


# In[7]:


# print(recognize_no_noise('audio/test1.wav'))


# Распознавание с учетом шума: уровень шума определяется автоматически

# In[8]:


def recognize_with_noise(audio_src):
    r = sr.Recognizer()

    # делим аудио на части
    chunks_src = divide_audio(audio_src)
    # распознаем каждую часть
    text_array = []
    for chunk_src in chunks_src:
        a = sr.AudioFile(chunk_src)
        # print('analyzing ', chunk_src)
        with a as source:
            r.adjust_for_ambient_noise(source)  # учитываем шум
            audio = r.record(source)
        try:
            text_chunk = r.recognize_google(audio, language="ru")
            text_array.append(text_chunk)
            # print(text_chunk)
        except:
            pass
    # объединяем распознанные тексты
    text = combine_text(text_array)
    # удаляем ненужные файлы
    delete_tmp_slices(chunks_src)

    return text


# In[9]:


# print(recognize_with_noise('audio/test1.wav'))


# Итоговая функция распознавания, в которой выбирается наилучший вариант распознавания

# In[10]:


def wav_to_txt(audio_src, out_txt_src, cursor):
    print(f"Speech recognition started")
    no_noise_txt = recognize_no_noise(audio_src)
    noise_txt = recognize_with_noise(audio_src)

    text = no_noise_txt
    if len(noise_txt.split()) > len(text.split()):
        text = noise_txt

    # записываем в файл
    out = open(out_txt_src, "a")
    out.write(text)
    out.close()
    print(f"Speech recognition finished")
    text_to_db(text, str(os.path.abspath(audio_src)), cursor)

# Для интеграции в main

# In[12]:


# wav_to_txt('audio/test1.wav', 'TEXT.txt')


# In[ ]:


if __name__ == "__main__":
    args = parser.parse_args()
    wav_to_txt(args.wav_path, args.out_path)

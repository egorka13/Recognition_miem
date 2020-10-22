# Recognition_miem

To run this script, you need to:

1. Install ffmpeg, pytesseract, cv2, pydub, pdf2image, SpeechRecognition
    ```bash
        sudo pip3 install ffmpeg-python pytesseract opencv-python pydub pdf2image SpeechRecognition 
    ```
2. Put your video file into the folder ./files in the root of the project
3. Run from cli
    ```bash
        python3 main.py -vi files/videoplayback.mp4 output.txt 1
    ```
    This command will convert video into the series of images with 1 frame per second.
    After that, array of images are going to be parsed into .txt file as text.
    
    ```bash
        python3 main.py -va files/videoplayback.mp4 output.txt
    ```
    This command will convert video into audio file of the format .wav.
    After that, audio file is going to be parsed into .txt file as text.
    
    ```bash
        python3 main.py -i files output.txt 
    ```
    This command will convert images in directory 'files' into .txt file as text.
    
    ```bash
        python3 main.py -a files/videoplayback.wav output.txt
    ```
    This command will convert audio file of the format .wav into .txt file as text.

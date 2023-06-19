import streamlit as st
import os
import shutil
from datetime import datetime
from pytube import YouTube
from moviepy.editor import VideoFileClip
import whisper
import pandas as pd
import pyperclip
from myfunctions import current_directory, create_folder_and_directories, download_youtube, rename_video, mp4_to_mp3, transcribe_mp3

st.set_page_config(layout="wide",
                   page_title='Transcribe YouTube Video',
                   page_icon=':video_camera:')


st.header('Transcribe YouTube Video :video_camera:')



current_directory(3)

# Specify the YouTube video URL
video_url = st.text_input('Youtube link', 'https://www.youtube.com/watch?v=8Zx04h24uBs&ab_channel=LexClips')
youtube_button = st.button('Transcribe')

if youtube_button:

    mp4_directory, mp3_directory, txt_directory = create_folder_and_directories()

    with st.spinner("Download Youtube as MP4"):
        download_youtube(video_url, mp4_directory)
     

    with st.spinner("Convert MP4 to MP3"):
        rename_video(mp4_directory)

        mp4_to_mp3(mp4_directory, mp3_directory)

        
    with st.spinner("Transcribe YouTube Video ... "):
        col1, col2 = st.columns(2)

        result = transcribe_mp3(mp3_directory)      


        col2.audio(f"{mp3_directory}/my_audio.mp3")
        col2.video(video_url)


        txt_path = f"{txt_directory}/output.txt" 

        # Open the file in write mode
        with open(txt_path, 'w') as file:
            # Write the data to the file
            file.write(result['text'])


        col1.info(f"Detected language: {result['language']}")


        
        for segment in result['segments']:
            start = round(float(segment['start']),2)
            end = round(float(segment['end']),2)
            text = segment['text']
            col1.markdown(f"""[{start} : {end}] : {text}""")

        


                                                                                        
        st.download_button('Download text as csv', result['text'])



    
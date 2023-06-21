import streamlit as st
import os
import shutil
from datetime import datetime, timedelta
from pytube import YouTube
from moviepy.editor import VideoFileClip
import whisper
import pandas as pd
import pyperclip
from myfunctions import current_directory, create_folder_and_directories, download_youtube, rename_videos, mp4_to_mp3, transcribe_mp3, with_opencv, concatenate_txt_files
import cv2
import glob
from io import BytesIO
from mutagen.mp3 import MP3
from pydub import AudioSegment

result = BytesIO()

st.set_page_config(layout="wide",
                   page_title='Transcribe Audio',
                   page_icon='	:loud_sound:')


st.header('Transcribe MP3 	:loud_sound:')



current_directory(3)



#if youtube_button:

try:
  # check if the key exists in session state
  _ = st.session_state.keep_graphics
except AttributeError:
  # otherwise set it to false
  st.session_state.keep_graphics = False


# Specify the YouTube video URL
# video_url = st.text_input('Youtube link', 'https://www.youtube.com/watch?v=8Zx04h24uBs&ab_channel=LexClips')
audio_file = st.file_uploader("Upload an audio file", type=["mp3"])

if audio_file is not None:
    youtube_button = st.button('Transcribe')

    if youtube_button or st.session_state.keep_graphics:
        
        audio_mp3 = MP3(audio_file)
        duration = audio_mp3.info.length

        mp4_directory, mp3_directory, txt_directory = create_folder_and_directories()


        
        
        if duration < 300 :# 5 minutes             
                
                col1, col2 = st.columns(2)
                
                col2.audio(audio_file)
                
                # Save the segment as an MP3 file
                audio_file = AudioSegment.from_file(audio_file)
                audio_file.export(f"{mp3_directory}/my_audio.mp3", format="mp3")
                with st.spinner("Transcribe Audio ... "):
                        result = transcribe_mp3(mp3_directory, "my_audio") 
        
                        txt_path = f"{txt_directory}/output.txt" 
        
                        # Open the file in write mode
                        with open(txt_path, 'w') as file:
                            # Write the data to the file
                            file.write(result['text'])

                with col1:
                    st.info(f"Detected language: {result['language']}")


                    
                    for segment in result['segments']:
                        start = round(float(segment['start']),2)
                        end = round(float(segment['end']),2)
                        text = segment['text']
                        st.markdown(f"""[{start} : {end}] : {text}""")

                    

                    user_text = col1.text_area("The Complete Text",result['text'], height=400)
                                                                                
                    #st.download_button('Download text as csv', result['text'])
                    st.download_button(
                            label=f"Download as txt",
                            data=result['text'],
                            file_name=f'Transcribe Audio {datetime.now()}.txt',
                            mime='text/plain'
                        )
            

        else:
                
                st.warning(f'The duration of the audio exceeds 5 minutes ({round(duration/60,2)} minutes). To handle this, the application will divide the audio into multiple 5-minute segments and convert each segment into an MP3 file. ', icon="⚠️")
                col1, col2 = st.columns(2)


                audio = AudioSegment.from_file(audio_file)
                duration = len(audio) / 1000  # Convert to seconds

                # Calculate the number of 5-minute segments
                num_segments = int(duration // 300) + 1
                result_text = ''
                
                

                for i in range(num_segments):
                    # Set the start and end times for the segment
                    start_time = i * 300 * 1000  # 5 minutes (converted to milliseconds)
                    end_time = min((i + 1) * 300 * 1000, len(audio))  # 5 minutes or remainder of the audio

                    # Extract the segment
                    segment = audio[start_time:end_time]

                    # Set the output filename for the segment
                    output_filename = f"segment_{i + 1}"

                    # Save the segment as an MP3 file
                    segment.export(f"{mp3_directory}/{output_filename}.mp3", format="mp3")

                    col2.audio(f"{mp3_directory}/segment_{i + 1}.mp3")

                    with st.spinner(f"Transcribe MP3 from : {start_time/1000/60} minute to {end_time/1000/60} minute"):

                        # Transcribe the MP3 segment using a function called transcribe_mp3
                        result = transcribe_mp3(mp3_directory,output_filename)

                    for segment in result['segments']:
                        start = round(float(segment['start']), 2)
                        end = round(float(segment['end']), 2)
                        text = segment['text']
                        col1.markdown(f"[{start}sec : {end}sec] : {text}")
                    col1.write('---')

                    result_text += result['text'] + " "

                


                #concatenated_text = concatenate_txt_files(txt_directory)
                #st.download_button('Download text as csv', concatenated_text)
                result = result_text
                user_text = col1.text_area("The Complete Text",result, height=400)
        
                col1.download_button(
                            label=f"Download as txt",
                            data=result,
                            file_name=f'Transcribe Audio {datetime.now()}.txt',
                            mime='text/plain'
                        )





    for i in range(20):
        st.write("")

    st.markdown("""
    ----
    **Contact** :

    If you have any questions, suggestions or bug to report, you can contact me via my email: [e.a.darwich@gmail.com](https://www.linkedin.com/in/e-darwich/)
    """)
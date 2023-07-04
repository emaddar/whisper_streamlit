import streamlit as st
import os
import shutil
from datetime import datetime, timedelta
from pytube import YouTube
from moviepy.editor import VideoFileClip
import whisper
import pandas as pd
import pyperclip
from my_functions import current_directory, create_folder_and_directories, transcribe_mp3
from my_summarization_functions import sample_extractive_summarization, sample_abstractive_summarization
from my_audio_functions import convert_to_mp3
import cv2
import glob
from io import BytesIO
from mutagen.mp3 import MP3
from pydub import AudioSegment

result = BytesIO()


st.set_page_config(layout="wide",
                   page_title='Transcribe Audio',
                   page_icon='	:loud_sound:')

# make any grid with a function
def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid


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
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "aac"])


if audio_file is not None:
    file_extension = os.path.splitext(audio_file.name)[1][1:].lower()
    


    youtube_button = st.button('Transcribe')

    if youtube_button or st.session_state.keep_graphics:

        with st.spinner("Please wait ..."):

            mp4_directory, mp3_directory, txt_directory = create_folder_and_directories()


            audio = AudioSegment.from_file(audio_file)
            audio.export(f"{mp3_directory}/my_audio.mp3", format="mp3")
            
            audio = f"{mp3_directory}/my_audio.mp3"
            audio_mp3 = MP3(audio)
            duration = audio_mp3.info.length
       

        


        
        
        if duration <= 180 :# 3 minutes             
                
                col1, col2 = st.columns(2)
                
                col2.audio(f"{mp3_directory}/my_audio.mp3")
                
                # Save the segment as an MP3 file
                # audio = AudioSegment.from_file(audio)
                # audio.export(f"{mp3_directory}/my_audio.{file_extension}", format="mp3")
                with st.spinner("Transcribe Audio ... "):
                        result = transcribe_mp3(mp3_directory, "my_audio") 
        
                        txt_path = f"{txt_directory}/output.txt" 
        
                        # Open the file in write mode
                        with open(txt_path, 'w') as file:
                            # Write the data to the file
                            file.write(result['text'])
                WebVTT = "WEBVTT"
                with col1:
                    st.info(f"Detected language: {result['language']}")


                    
                    for segment in result['segments']:
                        start = round(float(segment['start']),2)
                        end = round(float(segment['end']),2)
                        text = segment['text']
                        #st.markdown(f"""[{start} : {end}] : {text}""")
                        WebVTT += f""" \n[{start} : {end}] : {text}"""
                    
                with st.expander("WebVTT"):
                    st.text_area("Format Web Video Text Tracks (WebVTT)", WebVTT, height=200)

                    

                user_text = st.text_area("The Complete Text",result['text'], height=200)
                                                                            
                #st.download_button('Download text as csv', result['text'])
                st.download_button(
                        label=f"Download as txt",
                        data=result['text'],
                        file_name=f'Transcribe Audio {datetime.now()}.txt',
                        mime='text/plain'
                    )
        

        else:
                
                st.warning(f'The duration of the audio exceeds 3 minutes ({round(duration/60,2)} minutes). To handle this, the application will divide the audio into multiple 3-minute segments and convert each segment into an MP3 file. ', icon="⚠️")
                col1, col2 = st.columns(2)


                # Calculate the number of 5-minute segments
                num_segments = int(duration // 180) + 1
                result_text = ''
                
                
                WebVTT = "WEBVTT"
                for i in range(num_segments):
                    with col2:
                        with st.spinner("Please wait ..."):
                            # Set the start and end times for the segment
                            start_time = i * 180 * 1000  # 3 minutes (converted to milliseconds)
                            end_time = min((i + 1) * 180 * 1000, duration*1000)  # 3 minutes or remainder of the audio

                            audio_mp3 = AudioSegment.from_file(f"{mp3_directory}/my_audio.mp3")
                            # Extract the segment
                            segment = audio_mp3[start_time:end_time]

                            # Set the output filename for the segment
                            output_filename = f"segment_{i + 1}"

                            # Save the segment as an MP3 file
                            segment.export(f"{mp3_directory}/{output_filename}.mp3", format="mp3")
                        
                        st.audio(f"{mp3_directory}/segment_{i + 1}.mp3")

                    with st.spinner(f"Transcribe MP3 from : {round(start_time/1000/60,2)} minute to {round(end_time/1000/60,2)} minute"):

                        # Transcribe the MP3 segment using a function called transcribe_mp3
                        result = transcribe_mp3(mp3_directory,output_filename)
                    
                    
                    for segment in result['segments']:
                        start = round(float(segment['start']), 2)
                        end = round(float(segment['end']), 2)
                        text = segment['text']
                        #col1.markdown(f"[{start}sec : {end}sec] : {text}")
                        WebVTT += f" \n[{start}sec : {end}sec] : {text}"
                    col1.write(f"Transcribe MP3 from : {round(start_time/1000/60,2)} minute to {round(end_time/1000/60,2)} minute : OK" )

                    result_text += result['text'] + " "

                
                with col1:
                    st.info(f"Detected language: {result['language']}")
                with st.expander("WebVTT"):
                    st.text_area("Format Web Video Text Tracks (WebVTT)", WebVTT, height=200)


                #concatenated_text = concatenate_txt_files(txt_directory)
                #st.download_button('Download text as csv', concatenated_text)
                result = result_text


                txt_path = f"{txt_directory}/output.txt" 
        
                # Open the file in write mode
                with open(txt_path, 'w') as file:
                    # Write the data to the file
                    file.write(result)

                user_text = st.text_area("The Complete Text",result, height=200)
        
                st.download_button(
                            label=f"Download as txt",
                            data=result,
                            file_name=f'Transcribe Audio {datetime.now()}.txt',
                            mime='text/plain'
                        )

        txt_path = f"{txt_directory}/output.txt" 
        file = open(txt_path, "r")
        # Read the contents of the file
        file_contents = file.read()

        # Close the file
        file.close()
        
        # st.text_area("The Summarized Text",sample_extractive_summarization([file_contents]), height=400)
        # #st.text_area("The Summarized Text",file_contents, height=400)
        # st.write()

        mygrid0 = make_grid(1,2)
        with mygrid0[0][0]:
            with st.spinner("Extractive Summarization ..."):
                extractive_summarization = sample_extractive_summarization([file_contents])
            st.text_area("Extractive Summarization", extractive_summarization, height=200)
        with mygrid0[0][1]:
            with st.spinner("Abstractive Summarization ..."):
                abstractive_summarization = sample_abstractive_summarization([file_contents])
            st.text_area("Abstractive Summarization", abstractive_summarization, height=200)




    for i in range(20):
        st.write("")

    st.markdown("""
    ----
    **Contact** :

    If you have any questions, suggestions or bug to report, you can contact me via my email: [e.a.darwich@gmail.com](https://www.linkedin.com/in/e-darwich/)
    """)

import streamlit as st
import os
import shutil
from datetime import datetime
from pytube import YouTube
from moviepy.editor import VideoFileClip
import whisper
import pandas as pd
import pyperclip

st.set_page_config(layout="wide",
                   page_title='Transcribe YouTube Video',
                   page_icon=':video_camera:')


st.header('Transcribe YouTube Video :video_camera:')




# Get the current directory
current_directory = os.getcwd()

# Get a list of all directories in the current directory
directories = [name for name in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, name))]

# Filter directories that start with "My_Folder_"
matching_directories = [name for name in directories if name.startswith("Folder_")]

# Check if there are more than 3 matching directories
if len(matching_directories) > 3:
    # Remove the matching directories
    for directory in matching_directories:
        directory_path = os.path.join(current_directory, directory)
        shutil.rmtree(directory_path)
        print(f"Removed directory: {directory_path}")
else:
    print("There are not enough matching directories to remove.")





# # Specify the directory path
# mp4_path = 'medias/mp4'

# Specify the YouTube video URL
video_url = st.text_input('Youtube link', 'https://www.youtube.com/watch?v=8Zx04h24uBs&ab_channel=LexClips')
youtube_button = st.button('Transcribe')

if youtube_button:

    



    # Get the current date and time
    now = datetime.now()

    # Create a new folder with the current hour
    current_folder = f"Folder_{now.strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(current_folder)

    # Create the subdirectories within the current folder
    mp4_directory = os.path.join(current_folder, 'media', 'mp4')
    mp3_directory = os.path.join(current_folder, 'media', 'mp3')
    txt_directory = os.path.join(current_folder, 'media', 'txt')

    # Create the subdirectories
    os.makedirs(mp4_directory)
    os.makedirs(mp3_directory)
    os.makedirs(txt_directory)





    # Create a YouTube object
    yt = YouTube(video_url)

    # Get the lowest resolution video stream
    stream = yt.streams.get_lowest_resolution()

    # Download the video
    stream.download(mp4_directory)
    st.write('YouTube download ...................... OK')




    # Get a list of all files in the directory
    files = os.listdir(mp4_directory)

    # Iterate over each file and rename it
    for filename in files:
        # Construct the current file path
        current_path = os.path.join(mp4_directory, filename)
        
        # Split the current filename and extension
        name, extension = os.path.splitext(filename)
        
        # Construct the new filename
        new_name = 'video' + extension
        
        # Construct the new file path
        new_path = os.path.join(mp4_directory, new_name)
        
        # Rename the file
        os.rename(current_path, new_path)




        

    # # Specify the output path for the converted MP3 file
    # mp3_path = 'medias/mp3/my_audio.mp3'

    # Load the video file
    video = VideoFileClip(f"{mp4_directory}/video.mp4")

    # Extract the audio from the video file
    audio = video.audio

    # Save the audio as an MP3 file
    audio.write_audiofile(f"{mp3_directory}/my_audio.mp3", codec='mp3')

    # Close the video and audio files
    video.close()
    audio.close()

    st.write('Convert mp4 to mp3..................... OK')




    col1, col2 = st.columns(2)
    

    

    model = whisper.load_model("tiny")
    result = model.transcribe(f"{mp3_directory}/my_audio.mp3")
    print(result["text"])


    
    col2.audio(f"{mp3_directory}/my_audio.mp3")
    col2.video(video_url)






    txt_path = f"{txt_directory}/output.txt" 

    # Open the file in write mode
    with open(txt_path, 'w') as file:
        # Write the data to the file
        file.write(result['text'])

    # print("Data saved to", txt_path)



    col1.info(f"Detected language: {result['language']}")


    
    for segment in result['segments']:
        start = round(float(segment['start']),2)
        end = round(float(segment['end']),2)
        text = segment['text']
        col1.markdown(f"""[{start} : {end}] : {text}""")

    


                                                                                    
    st.download_button('Download text as csv', result['text'])



    
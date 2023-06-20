import os
import shutil
from datetime import datetime, timedelta
from pytube import YouTube
from moviepy.editor import VideoFileClip
import whisper
import cv2
import glob

@st.cache_data()
def current_directory(n):
    # Get the current directory
    current_directory = os.getcwd()

    # Get a list of all directories in the current directory
    directories = [name for name in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, name))]

    # Filter directories that start with "My_Folder_"
    matching_directories = [name for name in directories if name.startswith("Folder_")]

    # Check if there are more than n matching directories
    if len(matching_directories) > n:
        # Remove the matching directories
        for directory in matching_directories:
            directory_path = os.path.join(current_directory, directory)
            shutil.rmtree(directory_path)
            print(f"Removed directory: {directory_path}")
    else:
        print("There are not enough matching directories to remove.")



@st.cache_data()
def create_folder_and_directories():
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
    return mp4_directory, mp3_directory, txt_directory


@st.cache_data()
def download_youtube(video_url, mp4_directory):
        # Create a YouTube object
        yt = YouTube(video_url)

        # Get the lowest resolution video stream
        stream = yt.streams.get_lowest_resolution()

        # Download the video
        stream.download(mp4_directory)  



@st.cache_data()
def rename_video(mp4_directory):
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


@st.cache_data()
def rename_videos(mp4_directory):
    # Get a list of all files in the directory
    files = os.listdir(mp4_directory)

    if len(files) > 1:
        # Iterate over each file and rename it
        for i, filename in enumerate(files, start=1):
            # Construct the current file path
            current_path = os.path.join(mp4_directory, filename)

            # Split the current filename and extension
            name, extension = os.path.splitext(filename)

            # Construct the new filename with numbering
            new_name = f"video_{i}{extension}"

            # Construct the new file path
            new_path = os.path.join(mp4_directory, new_name)

            # Rename the file
            os.rename(current_path, new_path)
    elif len(files) == 1:
        # Rename the single file as "video"
        filename = files[0]
        current_path = os.path.join(mp4_directory, filename)
        new_name = "video" + os.path.splitext(filename)[1]
        new_path = os.path.join(mp4_directory, new_name)
        os.rename(current_path, new_path)
    else:
        # No files in the directory
        print("No files found in the directory.")

@st.cache_data()
def mp4_to_mp3(mp4_directory, mp3_directory):
     # Load the video file
    video = VideoFileClip(f"{mp4_directory}/video.mp4")

    # Extract the audio from the video file
    audio = video.audio

    # Save the audio as an MP3 file
    audio.write_audiofile(f"{mp3_directory}/my_audio.mp3", codec='mp3')

    # Close the video and audio files
    video.close()
    audio.close()


@st.cache_data()
def transcribe_mp3(mp3_directory, my_audio):
    model = whisper.load_model("tiny")
    result = model.transcribe(f"{mp3_directory}/{my_audio}.mp3")
    print(result["text"])
    return result






@st.cache_data()
def cut_and_convert_to_mp3(filename, mp3_directory, txt_directory):
    video = VideoFileClip(filename)
    duration = video.duration

    # Calculate the number of 2-minute segments
    num_segments = int(duration // 300) + 1

    for i in range(num_segments):
        # Set the start and end times for the segment
        start_time = i * 300  # 2 minutes
        end_time = min((i + 1) * 300, duration)  # 2 minutes or remainder of the video

        # Extract the segment and convert to MP3
        segment = video.subclip(start_time, end_time)
        output_filename = f"{mp3_directory}/segment_{i + 1}.mp3"
        segment.audio.write_audiofile(output_filename)

        result = transcribe_mp3(mp3_directory, f"segment_{i + 1}")


        txt_path = f"{txt_directory}/output_{i + 1}.txt" 
        # Open the file in write mode
        with open(txt_path, 'w') as file:
            # Write the data to the file
            file.write(result['text'])

    video.close()
    return result



@st.cache_data()
def with_opencv(filename):
    video = cv2.VideoCapture(filename)

    # count the number of frames
    frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    
    # calculate duration of the video
    seconds = round(frames / fps)
    video_time = timedelta(seconds=seconds).total_seconds()
    return video_time





@st.cache_data()
def concatenate_txt_files(directory):
    # Get a list of all text files in the directory
    txt_files = glob.glob(os.path.join(directory, "*.txt"))

    # Concatenate the contents of all text files
    concatenated_text = ""
    for txt_file in txt_files:
        with open(txt_file, "r") as file:
            text = file.read()
            concatenated_text += text

    return concatenated_text

import streamlit as st
import os
from datetime import datetime
from moviepy.editor import VideoFileClip
from myfunctions.my_functions import current_directory, create_folder_and_directories, download_youtube, rename_videos, mp4_to_mp3, transcribe_mp3, download_youtube1, get_video_info
from myfunctions.my_summarization_functions import sample_extractive_summarization, sample_abstractive_summarization, sample_recognize_to_annotated_text
from io import BytesIO
from annotated_text import annotated_text

result = BytesIO()

st.set_page_config(layout="wide",
                   page_title='Transcribe YouTube Video',
                   page_icon=':video_camera:')

# make any grid with a function
def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid

with st.sidebar:
    st.image('images/Robot_whisper2.jpg')

st.header('Transcribe YouTube Video :video_camera:')



current_directory(3)



#if youtube_button:

try:
  # check if the key exists in session state
  _ = st.session_state.keep_graphics
except AttributeError:
  # otherwise set it to false
  st.session_state.keep_graphics = False


# Specify the YouTube video URL
video_url = st.text_input('Youtube link', 'https://www.youtube.com/watch?v=8Zx04h24uBs&ab_channel=LexClips')
youtube_button = st.button('Transcribe')

if youtube_button or st.session_state.keep_graphics:
    info = get_video_info(video_url)
    st.write(info)
    
    

    mp4_directory, mp3_directory, txt_directory = create_folder_and_directories()

    with st.spinner("Download Youtube as MP4"):

        try:
            video_extension = download_youtube(video_url, mp4_directory)

        except:
            with st.spinner("Please wait, the application is currently unable to download the video in MP4 format. It is currently attempting to download the video in WebM format instead. This process may take some time. Thank you for your patience."):
                video_extension,duration= download_youtube1(video_url, mp4_directory)
                # duration= download_youtube1(video_url, mp4_directory)


        rename_videos(mp4_directory)
        video_mp4 = os.path.join(mp4_directory, f"video.{video_extension}")
        # video_mp4 = os.path.join(mp4_directory, "video.webm")

    # Check the duration of the video in seconds
    if duration < 180 :# 3 minutes
            
            with st.spinner("Convert MP4 to MP3"):
        
                
                mp4_to_mp3(mp4_directory, video_extension, mp3_directory )
                

                
            
            col1, col2 = st.columns(2)   

                    

            
            col2.audio(f"{mp3_directory}/my_audio.mp3")
            

            with st.spinner("Transcribe YouTube Video ... "):
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
                    WebVTT += f""" \n[{start} : {end}] : {text}"""
                

                user_text = st.text_area("The Complete Text",result['text'], height=450)
            
            with st.expander("WebVTT"):
                    st.text_area("Format Web Video Text Tracks (WebVTT)", WebVTT, height=200)

                

            col2.video(video_url)
                                                                            
            #st.download_button('Download text as csv', result['text'])
            st.download_button(
                    label=f"Download as txt",
                    data=result['text'],
                    file_name=f'Transcribe YouTube Video {datetime.now()}.txt',
                    mime='text/plain'
                )
    

    else:
            
            st.warning(f'The duration of the video exceeds 3 minutes ({round(duration/60,2)} minutes). To handle this, the application will divide the video into multiple 3-minute segments and convert each segment into an MP3 file. ', icon="⚠️")
            col1, col2 = st.columns(2)

                    
            video = VideoFileClip(video_mp4)
            duration = video.duration

            # Calculate the number of 3-minute segments
            num_segments = int(duration // 180) + 1
            result_text = ''
            WebVTT = "WEBVTT"
            for i in range(num_segments):
                
                    # Set the start and end times for the segment
                    start_time = i * 180  # 3 minutes
                    end_time = min((i + 1) * 180, duration)  # 3 minutes or remainder of the video
                    with st.spinner(f"Please wait ..."):
                        # Extract the segment and convert to MP3
                        segment = video.subclip(start_time, end_time)
                        output_filename = f"{mp3_directory}/segment_{i + 1}.mp3"
                        segment.audio.write_audiofile(output_filename)

                        col2.audio(f"{mp3_directory}/segment_{i + 1}.mp3")


                    with st.spinner(f"Transcribe from : {round(start_time/60,2)} min. to {round(end_time/60,2)} min."):
                        result = transcribe_mp3(mp3_directory, f"segment_{i + 1}")
                    col1.write(f"Transcribe from : {round(start_time/60,2)} min. to {round(end_time/60,2)} min. : OK")
                    for segment in result['segments']:
                        start = round(float(segment['start']),2)
                        end = round(float(segment['end']),2)
                        text = segment['text']
                        #col1.markdown(f"""[{start} : {end}] : {text}""")
                        WebVTT += f""" \n[{start} : {end}] : {text}"""


                    result_text = result_text + result['text'] + " "

            with col1:
                st.info(f"Detected language: {result['language']}")
                
            

            video.close()
            col2.video(video_url)


            #concatenated_text = concatenate_txt_files(txt_directory)
            #st.download_button('Download text as csv', concatenated_text)
            result = result_text

            txt_path = f"{txt_directory}/output.txt" 
    
            # Open the file in write mode
            with open(txt_path, 'w') as file:
                # Write the data to the file
                file.write(result)

            user_text = col1.text_area("The Complete Text",result, height=450)
            with st.expander("WebVTT"):
                    st.text_area("Format Web Video Text Tracks (WebVTT)", WebVTT, height=200)
      
            col1.download_button(
                        label=f"Download as txt",
                        data=result,
                        file_name=f'Transcribe YouTube Video {datetime.now()}.txt',
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

    annotated_text(*sample_recognize_to_annotated_text([file_contents]))
    print(sample_recognize_to_annotated_text([file_contents]))


for i in range(20):
    st.write("")

st.markdown("""
----
**Contact** :

If you have any questions, suggestions or bug to report, you can contact me via my email: [e.a.darwich@gmail.com](https://www.linkedin.com/in/e-darwich/)
""")

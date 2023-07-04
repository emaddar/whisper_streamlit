import streamlit as st
from io import BytesIO


result = BytesIO()

st.set_page_config(
                   page_title='Audio2Texte',
                   page_icon=':video_camera:'
                )


st.header('Audio 2 Text')

st.markdown("""
This application allows you to transcribe any YouTube video or audio file. It utilizes the tiny general-purpose speech recognition model called `Whisper`, developed by OpenAI. The application automatically detects the language.

You can check the source code at this [github repository](https://github.com/emaddar/whisper_streamlit)

Using this application is simple and straightforward : simply select the audio source and let this AI do the work :stuck_out_tongue_winking_eye:
""")
st.image('AI.jpg')
for i in range(2):
    st.write("")

st.markdown("""
----
**Contact** :

If you have any questions, suggestions or bug to report, you can contact me via my email: [e.a.darwich@gmail.com](https://www.linkedin.com/in/e-darwich/)
""")

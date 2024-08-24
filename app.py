import os
import asyncio
import edge_tts
import streamlit as st
from audio_recorder import live_audio_recorder
from QABert import return_final_answer

def load_css(file_name):
    with open(file_name, "r") as file:
        st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

output_dir = "audio_generated"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def text_to_speech(text, voice, rate):
    OUTPUT_FILE = 'audio_generated/answer.mp3'
    async def amain():
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(OUTPUT_FILE)
    asyncio.run(amain())

# Sidebar layout
st.sidebar.image("logos/voice-assistant-concept-illustration.png", use_column_width=True)
st.sidebar.markdown("---")

# Voice customization options
voice_character = st.sidebar.selectbox("Voice Character", ['Male', 'Female'])
speed = st.sidebar.selectbox("Speed", ['Slow', 'Medium', 'Fast'])


st.sidebar.markdown("### About")
st.sidebar.info("This is your AI Voice Assistant and it is created by Arya Chakraborty")
voice_map = {'Male': 'en-US-GuyNeural', 'Female': 'en-US-JennyNeural'}
speed_map = {'Slow': '-50%', 'Medium': '+1%', 'Fast': '+50%'}

VOICE = voice_map[voice_character]
RATE = speed_map[speed]


css_path = os.path.join('templates', 'style.css')
load_css(css_path)
st.markdown('<div class="center-top-container"><p class="custom-title"><span class="red-bold">Q</span>.U.E.S.T</p></div>', unsafe_allow_html=True)

col1,col2,col3 = st.columns([1.1,2,1])
with col3:
    option = st.radio("Input Options",["Voice Input", "File Input"],label_visibility="collapsed") 

with col2:
    st.caption("QBERT-Utilized Edge Speech Technology")
    if option == "Voice Input":
        start_button = st.button("Start the Voice Assistant",key="start_button")
    else:
        uploaded_audio_file = st.file_uploader("Upload your audio file",label_visibility="collapsed")


col4,col5,col6 = st.columns([0.1,2,0.1])
with col5:
    if option == "Voice Input":
            if start_button:
                audio_file = live_audio_recorder()
                question, answer = return_final_answer(audio_file)

                st.write('**Your Question:**', question)
                st.write('**Generated Answer:**', answer)

                text_to_speech(answer, VOICE, RATE)
                st.audio('audio_generated/answer.mp3')
    elif option == "File Input":
        if uploaded_audio_file is not None:
            file_name = uploaded_audio_file.name
            # Save the uploaded file to "audio_generated" directory
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, "wb") as f:
                f.write(uploaded_audio_file.getbuffer())
            
            st.success('File saved')
            st.audio(file_path)

            question, answer = return_final_answer(file_path)
            st.write('**Your Question:**', question)
            st.write('**Generated Answer:**', answer)
            text_to_speech(answer, VOICE, RATE)
            st.audio('audio_generated/answer.mp3')
        else:
            st.warning('Please upload a file')
        



    

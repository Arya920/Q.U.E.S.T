import pyaudio
import keyboard
import time
import wave
import streamlit as st

def live_audio_recorder():

    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000
    Output_Filename = "audio_generated/live_recorded.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    # Inform the user to press SPACE to start recording
    st.info("Press SPACE to start recording")
    keyboard.wait('space')

    st.warning("Recording... Press SPACE to stop.")
    time.sleep(0.2)

    with st.spinner("Recording..."):
        while True:
            try:
                data = stream.read(chunk)
                frames.append(data)
            except KeyboardInterrupt:
                break
            if keyboard.is_pressed('space'):
                st.warning("Stopping recording...")
                time.sleep(0.2)
                break

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(Output_Filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    st.success('Recording complete!')

    return Output_Filename

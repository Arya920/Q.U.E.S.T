import whisper
import streamlit as st
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from web_search import search_google

@st.cache_resource
def load_models():
    # Load Whisper model
    whisper_model = whisper.load_model("base")
    
    # Load QA model and tokenizer
    QAtokenizer = AutoTokenizer.from_pretrained("SRDdev/QABERT-small")
    QAmodel = AutoModelForQuestionAnswering.from_pretrained("SRDdev/QABERT-small")
    
    return whisper_model, QAmodel, QAtokenizer

def speech_to_text(voice_recording_path, whisper_model):
    result = whisper_model.transcribe(voice_recording_path)
    question = result["text"]
    return question

def generate_answer(question, context, QAmodel, QAtokenizer):
    ask = pipeline("question-answering", model=QAmodel, tokenizer=QAtokenizer)
    result = ask(question=question, context=context)
    return f"The Answer of your question is: '{result['answer']}'"

def return_final_answer(voice_recording_path):
    whisper_model, QAmodel, QAtokenizer = load_models()
    question = speech_to_text(voice_recording_path, whisper_model)
    context = search_google(question)
    answer = generate_answer(question, context, QAmodel, QAtokenizer)
    
    return question, answer

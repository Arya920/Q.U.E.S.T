import whisper
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline
from web_search import search_google

def speech_to_text(voice_recording__path):
    model = whisper.load_model("base")
    result = model.transcribe(voice_recording__path)
    question = result["text"]
    return question

def generate_answer(question, context):
    QAtokenizer = AutoTokenizer.from_pretrained("SRDdev/QABERT-small")
    QAmodel = AutoModelForQuestionAnswering.from_pretrained("SRDdev/QABERT-small")

    ask = pipeline("question-answering", model= QAmodel , tokenizer = QAtokenizer)
    result = ask(question=f"{question}", context=context)
    return f"The Answer of your question is: '{result['answer']}'"


def return_final_answer(voice_recording_path):
    question = speech_to_text(voice_recording_path)
    context = search_google(question)
    answer = generate_answer(question, context)

    return question,answer

import whisper

model = whisper.load_model("tiny.en")

def stt(file_path="output.wav"):
    return model.transcribe(file_path)['text']

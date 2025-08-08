from src.tts import tts 
from src.stt import stt

filepath = "output.wav"
tts('Hello, welcome to amazon alexa clone.       ', delete_file=False, file_path=filepath)
print(stt(filepath))

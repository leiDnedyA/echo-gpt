from src.tts import tts 
from src.stt import await_speech_command, stt_from_mic, init_mic

def callback():
    print("triggered result")
    exit(0)

init_mic()

await_speech_command(callback)


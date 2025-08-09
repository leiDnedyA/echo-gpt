from src.ai import get_openai_response
from src.tts import tts 
from src.stt import await_speech_command, stt_from_mic, init_mic

def callback():
    tts("What's up?")
    prompt = stt_from_mic(10)
    response = get_openai_response(prompt)
    tts(response)
    exit(0)

init_mic()
tts("Say, \"Hey, robot\", wait for my response, and then ask a question.")

await_speech_command(callback)


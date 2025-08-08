import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from kittentts import KittenTTS
import soundfile as sf
import subprocess
import os
m = KittenTTS("KittenML/kitten-tts-nano-0.1")
VOICE = 'expr-voice-3-f'
# available_voices : [  'expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f',  'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f' ]

def _tts(message, voice, file_path):
    audio = m.generate(message + '.    ', # added to ensure audio isn't cut off
                       voice=voice, speed=1.2)
    sf.write(file_path, audio, 24000)
    subprocess.run(['play', file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(file_path)


def tts(message, voice=VOICE, file_path='output.wav'):
    chunks = message.split('\n')
    for chunk in chunks:
        _tts(chunk, voice, file_path)

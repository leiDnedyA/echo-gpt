from kittentts import KittenTTS
import soundfile as sf
import subprocess
import os
m = KittenTTS("KittenML/kitten-tts-nano-0.1")
VOICE = 'expr-voice-4-f'
# available_voices : [  'expr-voice-2-m', 'expr-voice-2-f', 'expr-voice-3-m', 'expr-voice-3-f',  'expr-voice-4-m', 'expr-voice-4-f', 'expr-voice-5-m', 'expr-voice-5-f' ]

def play_sound(message, voice='expr-voice-4-f'):
    FILE_PATH = 'output.wav'
    audio = m.generate(message + '.    ', # added to ensure audio isn't cut off
                       voice=voice)
    sf.write(FILE_PATH, audio, 24000)
    subprocess.run(['play', FILE_PATH])
    os.remove(FILE_PATH)

import whisper
import pyaudio
import wave
import os

model = whisper.load_model("tiny.en")

def stt_from_file(file_path="output.wav") -> str:
    return str(model.transcribe(file_path)['text'])

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

def stt_from_mic(record_seconds=5, file_path=WAVE_OUTPUT_FILENAME) -> str:
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    result = stt_from_file(file_path)
    os.remove(file_path)

    return result

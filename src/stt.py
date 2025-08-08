import whisper
import pyaudio
import wave
import os

model = whisper.load_model("tiny.en")

def stt_from_file(file_path="output.wav") -> str:
    return str(model.transcribe(file_path)['text'])

CHUNK = 2048
RATE = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1
WAVE_OUTPUT_FILENAME = "output.wav"

device_index = 0

def _print_available_devices():
    p = pyaudio.PyAudio()
    print("Available Input Devices:")
    default_api_index = p.get_default_host_api_info()["index"]
    info = p.get_host_api_info_by_index(default_api_index)
    numdevices = int(info.get('deviceCount'))
    for i in range(numdevices):
        device_info = p.get_device_info_by_host_api_device_index(default_api_index, i)
        if device_info.get('maxInputChannels') > 0:
            print(f"Input Device ID: {i} - Name: {device_info.get('name')}")

def init_mic():
    _print_available_devices()
    global device_index 
    device_index = int(input("Which device id to use >"))

def stt_from_mic(record_seconds=5, file_path=WAVE_OUTPUT_FILENAME) -> str:
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=device_index)

    frames = []

    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK, exception_on_overflow=False)
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

def await_speech_command(callback, command="robot"):
    chunk_seconds = 5
    while True:
        speech = stt_from_mic(chunk_seconds)
        if command in speech.lower():
            callback()

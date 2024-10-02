import pyaudio
import numpy as np
from spleeter.separator import Separator

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open stream to capture audio from the virtual audio cable
input_stream = p.open(format=pyaudio.paFloat32,
                      channels=2,
                      rate=44100,
                      input=True,
                      input_device_index=0,  # Adjust index for virtual audio cable
                      frames_per_buffer=1024)

# Open stream to play processed audio
output_stream = p.open(format=pyaudio.paFloat32,
                       channels=2,
                       rate=44100,
                       output=True)

# Initialize Spleeter
separator = Separator('spleeter:2stems')

def process_audio(data):
    # Convert buffer to waveform format
    waveform = np.frombuffer(data, dtype=np.float32).reshape(-1, 2)
    # Separate vocals and accompaniment
    prediction = separator.separate(waveform)
    # Extract accompaniment (non-vocal parts)
    accompaniment = prediction['accompaniment']
    return accompaniment.tobytes()

# Capture, process, and play audio in real-time
while True:
    data = input_stream.read(1024)
    processed_data = process_audio(data)
    output_stream.write(processed_data)

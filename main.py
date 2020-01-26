'''
Basic pitch detection algorithm:
    - sample audio
    - perform fft
    - round to nearest standard pitch value
'''

# Math dependencies
from math import log2
from scipy.fftpack import fft
import numpy as np

# Audio processing
import pyaudio
import struct

# Pitch standards
A4 = 440
C0 = A4 * pow(2, -4.75)
note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def pitch(freq):
    if freq <= 0:
        return "NULL"
    h = round(12*log2(freq/C0))
    octave = h // 12
    n = h % 12
    return note_names[n] + str(octave)

# pyaudio constants
CHUNK = 1024 * 4            # samples per frame
FORMAT = pyaudio.paInt16    # 16 bit integer audio format
CHANNELS = 1                # single mic channel
RATE = 48000                # 48 kHz bitrate

# pyaudio class instance
p = pyaudio.PyAudio()

# pyaudio stream for mic input
stream = p.open (
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# loop:
#   read audio stream
#   process and format data
#   find predominant frequency
#   print standard pitch equivalent

while True:
    x = np.arange(0, 2 * CHUNK, 2)
    y = np.linspace(0, RATE // 2, CHUNK // 2)

    chunk_data = stream.read(CHUNK)
    chunk_data = struct.unpack(str(2 * CHUNK) + 'B', chunk_data)
    chunk_data = np.array(chunk_data, dtype='b')[::2] + 128

    fft_data = fft(np.array(chunk_data, dtype='int8') - 128)
    fft_data = np.abs(fft_data[0:int(CHUNK / 2)]) * 2 / (128 * CHUNK)
    fft_data = fft_data[1:]  # slice off undefined [0] index of fft

    dom_freq_index = np.where(fft_data == np.amax(fft_data))[0][0]
    print("Freq: {:>8.2f} | Amp: {:>6.2f} | Note: {:<4s}".format(y[dom_freq_index],
                                                fft_data[dom_freq_index],
                                                pitch(y[dom_freq_index])))



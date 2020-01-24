import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
from scipy.fftpack import fft

CHUNK = 1024 * 2            # samples per frame
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
    output=False,
    frames_per_buffer=CHUNK
)

# matplotlib figure and axes initialization
fig, ax = plt.subplots()
x_fft = np.linspace(0, RATE, CHUNK)    # number of frequencies
line, = ax.semilogx(x_fft, np.random.rand(CHUNK), '-', lw=2)   # initialize line object
ax.set_xlim(20, RATE / 2)

# index for plot animation
i = count()

def animate(i):
    # read binary data from audio stream
    data = stream.read(CHUNK, exception_on_overflow = False)

    #audio data being plotted as signed int:
    #data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    
    #convert to unsigned
    f = lambda x: x + 128 if x < 128 else x - 128
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype = 'b')[::2]
    data_int = np.array([f(x) for x in data_int])
    y_fft = fft(data_int)

    #plt.cla()
    #plt.semilogx(x_fft, np.abs(y_fft[0:CHUNK]) * 2 / 256)
    line.set_ydata(np.abs(y_fft[0:CHUNK]) / 256)
    ax = plt.gca()
    ax.set_ylim(0, 255)
    #ax.set_xlim(20, RATE / 2)

ani = FuncAnimation(plt.gcf(), animate, 1)
#animate(0)
#input("Press any key...")
plt.show()


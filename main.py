import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count

CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open (
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    #output= True,
    frames_per_buffer = CHUNK
)

fig, ax = plt.subplots()

i = count()

def animate(i):
    data = stream.read(CHUNK, exception_on_overflow = False)

    #audio data being plotted as signed int
    #data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    #convert to unsigned
    f = lambda x: x + 128 if x < 128 else x - 128
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data))[::2]
    data_int = np.array([f(x) for x in data_int])
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype = 'b')[::2] + 63

    plt.cla()
    plt.plot(data_int, '-')

ani = FuncAnimation(plt.gcf(), animate, 1)
#input("Press any key...")
plt.show()


    


'''
x = np.arange(0, 2 * CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))

while True:
    data = stream.read(CHUNK, exception_on_overflow = False)
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype = 'b')[::2] + 127
    line.set_ydata(data_int)
    fig.canvas.draw()
    fig.canvas.flush_events()


while True:
    data = stream.read(CHUNK, exception_on_overflow = False)
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype = 'b')[::2] + 63

#stream.stop_stream()
#stream.close()
#p.terminate()

    fig, ax = plt.subplots()
    ax.plot(data_int, '-')
    plt.show()
'''

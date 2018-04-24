import pyaudio
import numpy as np
import time
import random

def play(freqs, dura=1, vol=0.5):
    p = pyaudio.PyAudio()
    volume = vol     # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz, must be integer
    duration = dura / 2   # in seconds, may be float
    # generate samples, note conversion to float32 array
    base = np.arange(fs*duration)
    data = np.zeros(int(fs*duration))
    for f in freqs:
        data += np.sin(2*np.pi*base*f/fs)
    data /= len(freqs)
    samples = data.astype(np.float32)

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    # play. May repeat with different volume values (if done interactively) 
    stream.write(volume*samples)

    stream.stop_stream()
    stream.close()

    p.terminate()

#for f in [[261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00]]:
    #play(f)

#play((261.63, 329.63, 392.00))
#play((246.94, 293.66, 392.00))
#play((261.63, 329.63, 440.00))
#play((293.66, 392.00, 493.88))
#play((261.63, 329.63, 392.00, 523.25), 2)



def rgb_to_hsv(r, g, b):
    r_ = r / 255
    g_ = g / 255
    b_ = b / 255
    C_max = max(r_, g_, b_)
    C_min = min(r_, g_, b_)
    delta = C_max - C_min
    if delta == 0:
        H = 0
    elif C_max == r_:
        H = 60 * ((g_ - b_)/delta%6)
    elif C_max == g_:
        H = 60 * ((b_ - r_)/delta + 2)
    elif C_max == b_:
        H = 60 * ((r_ - g_)/delta + 4)
    if C_max == 0:
        S = 0
    else:
        S = delta / C_max
    V = C_max
    return (H, S, V)


def play_rgb(r, g, b):
    h, s, v = rgb_to_hsv(r, g, b)
    print(h, s, v)

    h /= 360

    note = 261.63 + h * (523.25 - 261.63)
    volume = s
    duration = int(v * 5)

    play((note,), dura=duration, vol=volume)


play_rgb(92, 240, 94) # Naver green
play_rgb(119, 25, 170) # Onenote purple

play_rgb(45, 150, 245) # Daum(mobile) blue
play_rgb(66, 103, 178) # Facebook blue

play_rgb(221, 53, 108) # Instagram pink

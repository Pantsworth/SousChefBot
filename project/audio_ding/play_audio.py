__author__ = 'DoctorWatson'
"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave, os
#this imports everything in project aka util
from . import *

def play_ding():
    CHUNK = 4
    #
    # if len(sys.argv) < 2:
    #     print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    #     sys.exit(-1)

    wf = wave.open(os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), "") + "ding.wav", 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=2,
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    #
    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

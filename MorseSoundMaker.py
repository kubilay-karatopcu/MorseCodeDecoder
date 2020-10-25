import math
import wave
import struct

class MorseSoundMaker:
    """
    This class turns a text Morse into Morse sound of form .wav  
    """

    def __init__(self):
        self.frate = 44100.00 #that's the framerate
        self.freq=800.0 #that's the frequency, in hertz
        self.duration_dot = 0.050 #seconds of file
        self.duration_dash = 0.150

    def makeSound(self, sentence, fname):
        freq=self.freq
        framerate=self.frate
        sentence += " "
        amp=8000.0 # amplitude
        sine_list=[]
        for elm in sentence:
            if elm == ".":
                for x in range(int(self.duration_dot * framerate)):
                    sine_list.append(math.sin(2*math.pi * freq * ( x/framerate)))
                for x in range(int(self.duration_dash * framerate)):
                    sine_list.append(math.sin(0.1))
            elif elm == "-":
                for x in range(int(self.duration_dash * framerate)):
                    sine_list.append(math.sin(2*math.pi * freq * ( x/framerate)))
                for x in range(int(self.duration_dash * framerate)):
                    sine_list.append(math.sin(0.1))
            elif elm == " ":
                for x in range(int(self.duration_dot * framerate * 3)):
                    sine_list.append(math.sin(0.1))
            elif elm == "/":
                for x in range(int(self.duration_dot * framerate * 7)):
                    sine_list.append(math.sin(0.1))
        # Open up a wav file
        wav_file=wave.open(fname,"w")
        # wav params
        nchannels = 1
        sampwidth = 2
        framerate = int(framerate)
        nframes= int(self.calculateDataSize(sentence))
        comptype= "NONE"
        compname= "not compressed"
        wav_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        #write on file
        for s in sine_list:
            wav_file.writeframes(struct.pack('h', int(s*amp/2)))
        print(f"File saved as {fname}")
        wav_file.close()

    def calculateDataSize(self, sentence):
        space_count = sentence.count(".") + sentence.count("-")
        return (sentence.count(" ") * 1.05) + (sentence.count(".") * 0.150) + (sentence.count("-") * 0.450)  + (space_count * 0.450)

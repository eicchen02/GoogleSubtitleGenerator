from pydub import AudioSegment
import os

#? Set file to be shortened
f = "../temp_aud/conversation.wav"
basename = os.path.basename(f)

#?Set time seconds to clip between here
t1_sec = 15
t2_sec = 30

t1 = t1_sec * 1000 #Works in milliseconds
t2 = t2_sec * 1000

try:
    target_path = '../YOUR_SHOW_FLDR/clipped_{}'.format(basename)

    newAudio = AudioSegment.from_wav(f)
    newAudio = newAudio[t1:t2]
    newAudio.export(target_path, format="wav") #Exports to a wav file in the current path.
    print("New file created at {}".format(target_path))
except:
    raise "File clipping failed lol"

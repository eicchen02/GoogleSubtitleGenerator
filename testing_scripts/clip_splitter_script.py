from pydub import AudioSegment
import os

#? Set file to be shortened
f = "YOUR_SHOW_FLDR/conversation2.mp4"
basename = os.path.basename(f).split(".")[0]

# #?Set time seconds to clip between here
t1_sec = 0
t2_sec = 127

t1 = t1_sec * 1000 #Works in milliseconds
t2 = t2_sec * 1000

try:
    target_path = 'YOUR_SHOW_FLDR/clipped_{}-{}_{}.wav'.format(t1_sec, t2_sec, basename)

    newAudio = AudioSegment.from_file(f)
    newAudio = newAudio[t1:t2]
    newAudio.export(target_path, format="wav") #Exports to a wav file in the current path.
    print("New file created at {}".format(target_path))
except:
    raise "File clipping failed lol"

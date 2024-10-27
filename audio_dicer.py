import os
import pydub
from pydub import AudioSegment
import math
from logging import getLogger

##Created by Lex Whalen 2/19/21
class AudioDicer():
    """Google Translate can only handle so much file size, so we need to slice up our audio into bite-sized pieces."""

    def __init__(self):
        self.CWD = os.getcwd()
        self.TEMP_SPLIT_AUD = os.path.join(self.CWD,"temp_split_aud")

        #amount to slow audio down by
        self.RATE = 0.9 

        self.log = getLogger('subtitle_logging')

    def get_duration(self,aud_segment):
        
        #returns the time of the audio file. This is used to split the audio evenly.
        return aud_segment.duration_seconds

    def speed_change(self,sound, speed=1.0):
        ####Credit to StackOverflow####


        # Manually override the frame_rate. This tells the computer how many
        # samples to play per second
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        })

        # convert the sound with altered frame rate to a standard frame rate
        # so that regular playback programs will work right. They often only
        # know how to play audio at standard frame rate (like 44.1k)
        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

    def slow_audio(self,audio, slow_percent):

        #slow the audio down 
        slowed = self.speed_change(audio, slow_percent)

        return slowed

    def convert_wav(self, raw_file):
        audio =  AudioSegment.from_file(raw_file)

        #get the total seconds as an upper bound
        total_secs = math.ceil(self.get_duration(audio))
        self.log.info("Total Length of {}: {} seconds".format(os.path.basename(raw_file), total_secs))

        #slow audio by self.RATE
        audio_export = self.slow_audio(audio, self.RATE)
        
        audio_export_path = raw_file
        audio_export.export(audio_export_path,format="wav")


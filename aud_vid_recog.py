import speech_recognition as sr
from audio_dicer import AudioDicer
import os
import time
import moviepy.editor as mp
import shutil
from logging import getLogger

##Created by Lex Whalen 2/19/21
class AudioVideoRecognizer():
    """Deals with audio recognition. Uses Google Translate for .wav files. If a video, converts to .wav then uses Google Translate."""

    def __init__(self):
        self.RECOG = sr.Recognizer()
        self.DICER = AudioDicer()
    
        "Set length of time to dice audio by"
        self.SECONDS = 30

        self.CWD = os.getcwd()
        self.TEMP_AUD = os.path.join(self.CWD,"temp_aud")
        if os.path.exists(self.TEMP_AUD):
            shutil.rmtree(self.TEMP_AUD)
        os.makedirs(self.TEMP_AUD)
        
        self.log = getLogger('subtitle_logging')

    def trash_file(self,file_path):
        #sends file to trash
        os.remove(file_path)

    def transcribe(self,file_name,lang):
        """Transcribes the audio. Returns a list of the words found in that audio segment."""

        self.log.info("Transcribing {}...".format(os.path.basename(file_name)))
        master_words = []
        with sr.AudioFile(file_name) as source: #use f.wav as aud source
            #TODO Insert timestamping here
            #? idk why this was originally decided to be 30s

            #get aud data, uses record to parse for every self.SECONDS (currently 30)
            remaining_duration = source.DURATION
            while remaining_duration > 0:
                old_remaining_duration = remaining_duration
                audio_length = 0
                if remaining_duration >= self.SECONDS:
                    audio_length = self.SECONDS
                else: 
                    audio_length = remaining_duration
                remaining_duration = round(remaining_duration - audio_length, 2)

                audio = self.RECOG.record(source, audio_length)   

                self.log.info("Current Slice: {} - {}".format(old_remaining_duration, remaining_duration))
                try:
                    #try to see if it can make the speech out
                    words = self.RECOG.recognize_google(audio,language = lang).split()
                    master_words += words
                    # print(words)

                    #TODO Come back later to parse api_call, it may have timestamps?
                    # api_call = self.RECOG.recognize_google(audio,language = lang, show_all = True)

                except sr.UnknownValueError: #speech was unintelligible
                    try: 
                        #second try is to see if it can make the speech out when slowed down slightly
                        audio_slowed = self.DICER.slow_audio(audio, 0.95)
                        words = self.RECOG.recognize_google(audio,language = lang).split()
                        master_words += words
                    except:
                        self.log.error("Could not understand audio")
        
                except sr.RequestError: #No connection to server
                    self.log.error("Operation failed, no connection to server or key isn't valid")

        #if list was empty produce warning
        if not master_words:
            self.log.warning("Audio clip \"%s\" returned with no words found!" %os.path.basename(file_name))
        return master_words





        #! Current issues: Can't use not finding words as an end state, have to use EOF somehow
        #! audio = self.RECOG.record(source, duration) is missing words after duration for some reason
                

    # 
    def from_file(self,f,lang, isVideo = False):

        # if not isVideo:
        #     #already working with only an audio file
        #     words = self.transcribe(f,lang)

        #     return words

        # elif isVideo:
            #convert to wav and read
            

        filename = os.path.basename(f)
        filename_no_extension = os.path.splitext(filename)[0]
        aud_path_name = "{}.wav".format(filename_no_extension)
        aud_path_abs = os.path.join(self.TEMP_AUD,aud_path_name)

        #! Needs to be reviewed in the future, im too tired rn
        #is video
        try:
            #? idk what line 81, 82 do and if necessary
            clip = mp.VideoFileClip(f)
            clip.audio.write_audiofile(aud_path_abs)
            self.DICER.convert_wav(aud_path_abs,aud_path_abs)
            self.log.info("%s is a video!" %filename)

        #is not video
        except:
            self.DICER.convert_wav(f,aud_path_abs)
            self.log.info("%s is an audio clip!" %filename)

            


        #self.transcribe returns a list of words found
        words = self.transcribe(aud_path_abs,lang)

        #throw away the temps 
        for f in os.listdir(self.TEMP_AUD):
            f_path = os.path.join(self.TEMP_AUD,f)

            self.trash_file(f_path)

        
        #finally return words
        return words







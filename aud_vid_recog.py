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
        with sr.WavFile(file_name) as source: #use f.wav as aud source
            #TODO Insert timestamping here
            #get aud data, uses record to parse for every self.SECONDS (currently 30)
            while audio := self.RECOG.record(source, self.SECONDS):                  
                try:
                    #first try is to see if google recognizes that it is speech
                    try:
                        #second try is to see if it can make the speech out
                        words = [i for i in self.RECOG.recognize_google(audio,language = lang).split()]
                        master_words += words
                        #TODO Come back later to parse api_call, it may have timestamps?
                        # api_call = self.RECOG.recognize_google(audio,language = lang, show_all = True)

                    except Exception as e:
                        #no more words found in audio, return current list of words found so far.

                        return master_words

                except LookupError: #unintelligible
                    print("Could not understand audio")

    # 
    def from_file(self,f,lang, isVideo = False):

        if not isVideo:
            #already working with only an audio file
            words = self.transcribe(f,lang)

            return words

        elif isVideo:
            #convert to wav and read
            
            filename = os.path.basename(f)
            filename_no_extension = os.path.splitext(filename)[0]
            aud_path_name = "{}.wav".format(filename_no_extension)
            aud_path_abs = os.path.join(self.TEMP_AUD,aud_path_name)

            clip = mp.VideoFileClip(f)
            clip.audio.write_audiofile(aud_path_abs)

            self.DICER.convert_wav(aud_path_abs)

            #self.transcribe returns a list of words found
            words = self.transcribe(aud_path_abs,lang)

            #throw away the temps 
            for f in os.listdir(self.TEMP_AUD):
                f_path = os.path.join(self.TEMP_AUD,f)

                self.trash_file(f_path)

            
            #finally return words
            return words







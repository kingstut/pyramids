import torchaudio
from core import AudioCore
from sx import *

class AudioProject(AudioCore):
    def __init__(self):
        super().__init__(total_len=250, sample_rate=44100)
        self.audio_folder = '/Users/stuti/Documents/gopala/'

        # Intro
        self.tracks += [{
            'path' : self.audio_folder + 'waves.wav',
            'start' : 0,
            'end' : 51, 
            'loops' : 1, 
            'position' : 0,
            'sx' : [fade_out(self.sample_rate, 5)]
        }]
        self.tracks += [{
            'path' : self.audio_folder + 'nauka.mp3',
            'start' : 0,
            'end' : 21, 
            'loops' : 1, 
            'position' : 20,
            'sx' : [fade_in(self.sample_rate, 5), fade_out(self.sample_rate, 5)]
        }]

        # Beat drop
        self.tracks += [{
            'path' : self.audio_folder + 'tabla.wav',
            'start' : 0,
            'end' : None, 
            'loops' : 1, 
            'position' : 51,
            'sx' : []
        }]
        self.tracks += [{
            'path' : self.audio_folder + 'tabla.wav',
            'start' : 40,
            'end' : 54, 
            'loops' : 1, 
            'position' : 51 + 50,
            'sx' : [fade_in(self.sample_rate, 3)]
        }]
        self.tracks += [{
            'path' : self.audio_folder + 'tabla.wav',
            'start' : 40,
            'end' : 52, 
            'loops' : 1, 
            'position' : 51 + 52,
            'sx' : [fade_in(self.sample_rate, 3), delay()]
        }]

        # First vocal 
        self.tracks += [{
            'path' : self.audio_folder + 'govinda_pitch_-2.wav',
            'start' : 0,
            'end' : 36, 
            'loops' : 1, 
            'position' : 125,
            'sx' : [delay()]
        }]

        self.tracks += [{
            'path' : self.audio_folder + 'waves.wav',
            'start' : 0,
            'end' : None, 
            'loops' : 1, 
            'position' : 125 + 18,
            'sx' : [fade_in(self.sample_rate, 5), delay()]
        }]      

        # Background vocals 

        self.tracks += [{
            'path' : self.audio_folder + 'nauka.mp3',
            'start' : 3*60 + 29,
            'end' : 3*60 + 52, 
            'loops' : 2, 
            'position' : 125 + 36,
            'sx' : [fade_in(self.sample_rate, 5), compressor(), fade_out(self.sample_rate, 5), reverb]
        }]   

        # Bridge 
        self.tracks += [{
            'path' : self.audio_folder + 'govinda_pitch_-2.wav',
            'start' : 36,
            'end' : None, 
            'loops' : 1, 
            'position' : 125 + 36 + 2*(52-29),
            'sx' : [fade_in(self.sample_rate, 5), fade_out(self.sample_rate, 5)]
        }]       


        # Coda 




project = AudioProject()
track = project.render()

output_path = project.audio_folder + 'track.wav'
torchaudio.save(output_path, track, project.sample_rate)


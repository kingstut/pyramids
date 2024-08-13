from core import AudioCore
import torchaudio
from sx import *

class AudioProject(AudioCore):
    def __init__(self):
        super().__init__(total_len=80, sample_rate=14400)
        self.tracks += [{
            'path' : '',
            'start' : 0,
            'end' : 0, 
            'loops' : 1, 
            'position' : 5,
            'sx' : [delay(), reverb(0)]
        }]


project = AudioProject()
track = project.render()

output_path = ''
torchaudio.save(output_path, track, project.sample_rate)


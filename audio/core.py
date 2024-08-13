import torch
import torchaudio
import torchaudio.functional as F

class AudioCore():
    def __init__(self, total_len, sample_rate):
        self.total_len = total_len 
        self.sample_rate = sample_rate 
        self.track = torch.zeros(1, self.sample_rate*self.total_len)
        self.chunks = []
        self.tracks = []

    def match_sample_rate(self, sr, waveform):
        if sr != self.sample_rate:
            waveform = torchaudio.functional.resample(waveform, sr, self.sample_rate)
        
    def process_file(self, file_path, start_time=0, end_time=None, loops=1, sx=None):
        waveform, sr = torchaudio.load(file_path)

        # resample to match sample rate
        self.match_sample_rate(sr, self.sample_rate, waveform)
        
        # L and R
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
        
        # set start and end frame 
        start_frame = int(start_time * self.sample_rate)
        end_frame = int(end_time * self.sample_rate) if end_time else waveform.shape[1]

        # get chunk of audio 
        audio_chunk = waveform[:, start_frame: end_frame].repeat(loops, dim=1)

        # apply sx
        if sx:
            for effect in sx:
                audio_chunk = effect(audio_chunk)

        return audio_chunk
    
    def add_chunk(self, audio_chunk, position):
        self.chunks.append({'position': position, 'chunk': audio_chunk})

    def layer_audio(self):
        for config in self.chunks:
            start_frame = int(config['start'] * self.sample_rate)
            end_frame = start_frame + config['chunk'].shape[1] #int(config['end'] * self.sample_rate)
            self.track[:, start_frame:end_frame] += config['chunk']

    def render(self):
        # process
        for track in self.tracks:
            self.add_chunk(self.process_file(track['path'], track['start'], track['end'], track['loops'], track['sx']), track['position'])
        
        # layer 
        self.layer_audio()

        # normalize
        self.track = self.track / torch.max(torch.abs(self.track))
        return self.track





import torch
import torchaudio
import torchaudio.transforms as T
import torchaudio.functional as F

def compressor(threshold=-20.0, ratio=4.0):
    def apply_compressor(waveform):
        # Convert threshold from dB to amplitude
        threshold = 10 ** (threshold / 20)
        # Compute the compression
        compressed_waveform = torch.where(waveform > threshold, threshold + (waveform - threshold) / ratio, waveform)
        compressed_waveform = torch.where(compressed_waveform < -threshold, -threshold + (compressed_waveform + threshold) / ratio, compressed_waveform)
        return compressed_waveform
    return apply_compressor

def reverb(impulse_response=None):
    def apply_reverb(waveform):
        if impulse_response is None:
            impulse_response = torch.randn_like(waveform) 
        return F.fftconvolve(waveform, impulse_response)
    return apply_reverb

def time_stretch(time_stretch_factor):

    def apply_time_stretch(waveform):
        # Step 1: Convert waveform to a complex spectrogram
        stft = torch.stft(waveform, n_fft=1024, hop_length=None, return_complex=True)
        
        # Step 2: Apply time-stretching
        time_stretch = T.TimeStretch(hop_length=None, n_freq=stft.size(1))
        stretched_stft = time_stretch(stft, time_stretch_factor)
        
        # Step 3: Convert back to waveform
        stretched_waveform = torch.istft(stretched_stft, n_fft=1024, hop_length=None)
        
        return stretched_waveform

    return apply_time_stretch

def change_pitch(sample_rate, n_steps = -4):
    def apply_change_pitch(waveform):
        pitch_shift = T.Resample(orig_freq=int(sample_rate), new_freq=int(sample_rate * (2 ** (n_steps / 12))))
        return pitch_shift(waveform)
    return apply_change_pitch

def highpass_filter(sample_rate, cutoff_freq=100.0):
    def apply_highpass_filter(waveform):
        return F.highpass_biquad(waveform, sample_rate, cutoff_freq)
    return apply_highpass_filter

def lowpass_filter(sample_rate, cutoff_freq=5000.0):
    def apply_lowpass_filter(waveform):
        return F.lowpass_biquad(waveform, sample_rate, cutoff_freq)
    return apply_lowpass_filter 

def tremolo(sample_rate, speed=5.0, depth=0.5):
    def apply_tremolo(waveform):   
        tremolo = torchaudio.transforms.Tremolo(sample_rate, speed, depth)
        return tremolo(waveform)
    return apply_tremolo

def distortion(gain=20, threshold=0.5):
    def apply_distortion(waveform):
        waveform = waveform * gain
        return torch.clamp(waveform, -threshold, threshold)
    return apply_distortion

# def chorus(sample_rate, depth=0.5, rate=1.5):
#     def apply_chorus(waveform):
#         chorus = torchaudio.transforms.Chorus(sample_rate, depth, rate)
#         return chorus(waveform)
#     return apply_chorus

def delay(delay_samples=5000, decay=0.5):
    def apply_delay(waveform):
        delayed_waveform = torch.zeros_like(waveform)
        delayed_waveform[:, delay_samples:] = waveform[:, :-delay_samples] * decay
        return waveform + delayed_waveform
    return apply_delay 

def fade_in(sample_rate, duration):
    def apply_fade_in(waveform):
        num_samples = int(duration * sample_rate)
        fade_curve = torch.linspace(0, 1, num_samples).unsqueeze(0)
        waveform[:, :num_samples] *= fade_curve
        return waveform
    return apply_fade_in

def fade_out(sample_rate, duration):
    def apply_fade_out(waveform):
        num_samples = int(duration * sample_rate)
        fade_curve = torch.linspace(1, 0, num_samples).unsqueeze(0)
        waveform[:, -num_samples:] *= fade_curve
        return waveform
    return apply_fade_out
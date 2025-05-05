import numpy as np

class FFTProcessor:
    def __init__(self, sample_rate=16000, frame_size=2048):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.freqs = np.fft.rfftfreq(frame_size, d=1.0 / sample_rate)

    def compute_magnitude_spectrum(self, frame):
        fft_result = np.fft.rfft(frame)
        magnitude = np.abs(fft_result)
        return magnitude

    def get_frequency_bins(self):
        return self.freqs

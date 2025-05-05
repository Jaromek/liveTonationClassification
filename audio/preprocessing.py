import numpy as np

class AudioPreprocessor:
    def __init__(self, sample_rate=16000, frame_size=2048, hop_size=512):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size

    def stereo_to_mono(self, audio_data):
        if audio_data.ndim == 2:
            return np.mean(audio_data, axis=1).astype(np.float32)
        return audio_data

    def normalize(self, audio_data, eps=1e-9):
        peak = np.max(np.abs(audio_data))
        return audio_data / (peak + eps) if peak > 0 else audio_data

    def apply_hanning(self, frame):
        return frame * np.hanning(len(frame))



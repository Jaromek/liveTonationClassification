import numpy as np
import librosa

class AudioPreprocessor:
    def __init__(self, sample_rate=16000, frame_size=2048, hop_size=512):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size

    def load_audio(self, file_path):
        audio_data, sr = librosa.load(file_path, sr=self.sample_rate)
        return audio_data, sr

    def stereo_to_mono(self, audio_data):
        if audio_data.ndim == 2:
            return np.mean(audio_data, axis=1)
        return audio_data

    def normalize(self, audio_data):
        return audio_data / np.max(np.abs(audio_data)) if np.max(np.abs(audio_data)) > 0 else audio_data

    def hanning_window(self, audio_data):
        return np.hanning(len(audio_data)) * audio_data

    def frame_audio(self, audio_data):
        frames = librosa.util.frame(audio_data, frame_length=self.frame_size, hop_length=self.hop_size)
        return frames

    def preprocess(self, file_path):
        audio_data = self.load_audio(file_path)
        audio_data = self.stereo_to_mono(audio_data)
        audio_data = self.normalize(audio_data)

        frames = self.frame_audio(audio_data)

        windowed_frames = frames * np.hanning(self.frame_size)[:, None]
        
        return windowed_frames

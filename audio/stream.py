import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sounddevice as sd
import numpy as np
import collections
from audio.preprocessing import AudioPreprocessor
from signalProcessing.pitchDetection import PitchDetector
from model.keyClassifier import keyClassifier



class AudioStreamer:
    def __init__(self, sample_rate=16000, frame_size=2048, hop_size=512):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size
        self.preprocessor = AudioPreprocessor(sample_rate, frame_size, hop_size)
        self.pitch_detector = PitchDetector(sample_rate, frame_size)
        self.buffer = np.array([], dtype=np.float32)
        self.stream = None
        
        self.pitch_histogram = np.zeros(12, dtype=int)        
        self.window_size = 10
        self.analysis_interval = 10 * self.window_size
        self.pitch_history = collections.deque(maxlen=self.analysis_interval)
        
        self.key_classifier = keyClassifier(self.pitch_histogram)
        
        self.note_to_index = {v: k for k, v in self.key_classifier.key_map.items()}
        
        self.frame_counter = 0
        
        
        self.current_key = None
        self.current_mode = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print("Status: ", status)

        audio_chunk = indata[:, 0]
        print(f"Received chunk of size: {audio_chunk.shape[0]} samples")

        self.buffer = np.concatenate((self.buffer, audio_chunk))

        while len(self.buffer) >= self.frame_size:
            frame = self.buffer[:self.frame_size]
            self.buffer = self.buffer[self.hop_size:]

            frame = self.preprocessor.normalize(frame)
            windowed = self.preprocessor.apply_hanning(frame)

            rms = np.sqrt(np.mean(windowed**2))
            print(f"Frame RMS: {rms:.4f}")

            freq, note, octave = self.pitch_detector.detect_pitch(windowed)
            print(f"Dominujący ton: {note}{octave} ({freq:.2f} Hz)")
            
            if note in self.note_to_index:
                note_index = self.note_to_index[note]
                self.pitch_history.append(note_index)
                
                self.update_histogram()
                print(f"Histogram dźwięków: {self.pitch_histogram}")
            
            self.frame_counter += 1
            if self.frame_counter >= self.analysis_interval:
                self.analyze_key()
                self.frame_counter = 0

    def update_histogram(self):
        self.pitch_histogram = np.zeros(12, dtype=int)
        for note_idx in self.pitch_history:
            self.pitch_histogram[note_idx] += 1

    def analyze_key(self):
        if np.sum(self.pitch_histogram) > 0:
            predicted_key = self.key_classifier.classify(self.pitch_histogram)
            self.current_key = predicted_key
            self.current_mode = self.key_classifier.mode
            print(f"\nAktualna analiza tonacji: {predicted_key} ({self.current_mode})")
            print(f"Histogram dźwięków: {self.pitch_histogram}\n")

    def reset_histogram(self):
        self.pitch_histogram = np.zeros(12, dtype=int)
        self.pitch_history.clear()

    def start_stream(self):
        print("Streaming audio... Press Ctrl+C to stop.")
        print(f"Używam ruchomego okna o długości {self.window_size} dźwięków")
        print(f"Analiza tonacji co {self.analysis_interval} ramek")

        devices = sd.query_devices()
        print("Available audio devices:")
        for i, device in enumerate(devices):
            print(f"{i}: {device['name']}")

        device_info = sd.query_devices(kind='input')
        print(f"Using input device: {device_info['name']}")

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            blocksize=self.hop_size,
            dtype='float32',
            callback=self.audio_callback
        )

        self.stream.start()

        try:
            while True:
                sd.sleep(1000)
        except KeyboardInterrupt:
            self.stop_stream()

    def stop_stream(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
        print("Stream stopped.")

if __name__ == "__main__":
    streamer = AudioStreamer(sample_rate=16000, frame_size=2048, hop_size=512)
    streamer.start_stream()
    print(streamer.key_classifier.get_key(), streamer.key_classifier.get_mode())
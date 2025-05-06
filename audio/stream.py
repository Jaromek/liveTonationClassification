import sounddevice as sd
import numpy as np
from preprocessing import AudioPreprocessor
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from signalProcessing.pitchDetection import PitchDetector



class AudioStreamer:
    def __init__(self, sample_rate=16000, frame_size=2048, hop_size=512):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size
        self.preprocessor = AudioPreprocessor(sample_rate, frame_size, hop_size)
        self.pitch_detector = PitchDetector(sample_rate, frame_size)
        self.buffer = np.array([], dtype=np.float32)
        self.stream = None

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

    def start_stream(self):
        print("Streaming audio... Press Ctrl+C to stop.")

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

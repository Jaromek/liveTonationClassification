import sounddevice as sd
import numpy as np
from preprocessing import AudioPreprocessor

class AudioStreamer:
    def __init__(self, sample_rate=16000, frame_size=2048, hop_size=512):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size
        self.preprocessor = AudioPreprocessor(sample_rate, frame_size, hop_size)
        self.buffer = np.array([], dtype=np.float32)
        self.stream = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print("Status: ", status)

        # Odczyt danych audio (kanał 0 - mono)
        audio_chunk = indata[:, 0]

        # Debug: Sprawdzenie długości danych
        print(f"Received chunk of size: {audio_chunk.shape[0]} samples")

        # Łączenie nowych danych z poprzednimi
        self.buffer = np.concatenate((self.buffer, audio_chunk))

        # Przetwarzanie ramek
        while len(self.buffer) >= self.frame_size:
            frame = self.buffer[:self.frame_size]
            self.buffer = self.buffer[self.hop_size:]

            # Normalizacja i okno Hanninga
            frame = self.preprocessor.normalize(frame)
            windowed = frame * np.hanning(self.frame_size)

            # Analiza RMS
            rms = np.sqrt(np.mean(windowed**2))
            print(f"Frame RMS: {rms:.4f}")

    def start_stream(self):
        print("Streaming audio... Press Ctrl+C to stop.")
        
        # Sprawdzenie dostępnych urządzeń audio
        devices = sd.query_devices()
        print("Available audio devices:")
        for i, device in enumerate(devices):
            print(f"{i}: {device['name']}")

        # Sprawdzenie, czy mikrofon jest dostępny
        device_info = sd.query_devices(kind='input')
        print(f"Using input device: {device_info['name']}")

        # Rozpoczęcie strumienia audio
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

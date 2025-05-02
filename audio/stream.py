import sounddevice as sd
from preprocessing import AudioPreprocessor

class AudioStreamer:
    def __init__(self, sample_rate=16000, frame_size=2048, hop_size=512):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size
        self.preprocessor = AudioPreprocessor(sample_rate, frame_size, hop_size)
        self.stream = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        audio_data = indata[:, 0]
        windowed_frames = self.preprocessor.preprocess(audio_data)

    def start_stream(self):
        print("Streaming audio...")
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            blocksize=self.frame_size,
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
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
        print("Stream stopped.")


if __name__ == "__main__":
    streamer = AudioStreamer(sample_rate=16000, frame_size=2048, hop_size=512)
    streamer.start_stream()
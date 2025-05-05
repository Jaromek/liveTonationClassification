import numpy as np
from signal_processing.fft import FFTProcessor

NOTE_NAMES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
]

class PitchDetector:
    def __init__(self, sample_rate=16000, frame_size=2048):
        self.fft_processor = FFTProcessor(sample_rate, frame_size)

    def detect_pitch(self, frame):
        """
        Wykrywa dominującą częstotliwość i zwraca nutę oraz numer oktawy.

        Parametry:
            frame (np.ndarray): przetworzona ramka (mono, znormalizowana, okno Hanninga)

        Zwraca:
            tuple: (częstotliwość Hz, nuta, oktawa)
        """
        magnitude = self.fft_processor.compute_magnitude_spectrum(frame)
        dominant_idx = np.argmax(magnitude)
        freq = self.fft_processor.get_frequency_bins()[dominant_idx]

        note, octave = self._freq_to_note(freq)
        return freq, note, octave

    def _freq_to_note(self, freq):
        """
        Przelicza częstotliwość na najbliższą nutę i oktawę.
        """
        if freq <= 0:
            return "?", -1

        # A4 = 440 Hz, MIDI note = 69
        midi = int(round(69 + 12 * np.log2(freq / 440.0)))
        note_name = NOTE_NAMES[midi % 12]
        octave = midi // 12 - 1  # MIDI 60 = C4, czyli oktawa 4
        return note_name, octave

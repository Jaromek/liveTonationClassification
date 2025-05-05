import numpy as np
class ChromaFeatureExtractor:
    def __init__(self, sr=22050, n_chroma=12):
        self.sr = sr
        self.n_chroma = n_chroma

    def
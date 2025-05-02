class FFTProcessor:
    def __init__(self, data):
        self.data = data

    def compute_fft(self):
        from scipy.fft import fft
        return fft(self.data)

    def compute_ifft(self):
        from scipy.fft import ifft
        return ifft(self.data)
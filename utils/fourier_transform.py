import numpy as np
import matplotlib.pyplot as plt

from utils import audio


CHUNK = audio.CHUNK

class FourierTransform:
    f_ratio = 0.2
    data = audio.DATAINT
    sr = audio.RATE
    signal = np.array(data)
    """
    Peform Fourier Transform and Plot the Graph
    """
    def __init__(self):
        pass

    @classmethod
    def fourier_transform(cls):
        sig_fft = np.fft.fft(cls.signal)
        sig_fft_mag = np.absolute(sig_fft)

        f = np.linspace(0, cls.sr, len(sig_fft_mag))
        f_bins = int(len(sig_fft_mag)*cls.f_ratio)

        fig, ax = plt.subplots()
        line, = ax.plot(sig_fft, np.random.rand(CHUNK), 'r')
        ax.plot(f[:f_bins], sig_fft_mag[:f_bins])
        ax.set_xlabel('Frequency (Hz)')
        fig.show()

        while True:
            line.set_ydata(audio.DATAINT)
            fig.canvas.draw()
            fig.canvas.flush_events()



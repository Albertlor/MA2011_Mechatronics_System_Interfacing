import matplotlib.pyplot as plt
import numpy as np
import pyaudio as pa
import struct
import time
import json

from utils.traffic_light import Traffic


CHUNK = 1024*2
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100 # in Hz
T = 1.0 / 44100 # in s
t = np.linspace(0, CHUNK * T, CHUNK, endpoint=True)
f_ratio = 1


class Audio:
    dataInt = ()
    
    def __init__(self):
        pass

    @classmethod
    def sound_wave(cls):
        p = pa.PyAudio()

        stream = p.open(
            format = FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=True,
            frames_per_buffer=CHUNK
        )

        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        x = np.arange(0, 2*CHUNK, 2)
        line1, = ax[0].plot(x, np.random.rand(CHUNK), 'r')
        line2, = ax[1].plot(x, np.random.rand(CHUNK), 'b')
        
        fig.show()

        while True:
            data = stream.read(CHUNK)
            cls.dataInt = struct.unpack(str(CHUNK) + 'h', data)
            line1.set_ydata(cls.dataInt)
            line1.set_xdata(t)
            ax[0].set_ylim(-60000, 60000)
            ax[0].set_xlim(0, t[-1])
            ax[0].set_xlabel('Time (s)')
            ax[0].set_ylabel('Amplitude')

            normalized_data = Audio.normalize(cls.dataInt)
            signal = np.array(normalized_data)
            sig_fft = np.fft.fft(signal)
            sig_fft_mag = np.absolute(sig_fft)
            # f = np.linspace(0, RATE, len(sig_fft_mag))
            # f_bins = int(len(sig_fft_mag)*f_ratio)
            denormalized_data = Audio.denormalize(sig_fft_mag)

            line2.set_ydata(denormalized_data)
            line2.set_xdata(np.fft.fftfreq(len(denormalized_data), t[1]-t[0]))
            ax[1].set_ylim(-60000, 60000)
            ax[1].set_xlabel('Frequency (Hz)')
            ax[1].set_ylabel('Content')

            fig.canvas.draw()
            fig.canvas.flush_events()

            # print(f'x data: {np.fft.fftfreq(len(denormalized_data), t[1]-t[0])}')
            # print(f'denormalize: {denormalized_data}')

            Audio.special_vehicle([np.fft.fftfreq(len(denormalized_data), t[1]-t[0]), denormalized_data])


    @staticmethod
    def normalize(signal):
        mean = np.mean(signal)
        std = np.std(signal)
        return (signal - mean) / std

    @staticmethod
    def denormalize(signal):
        mean = np.mean(signal)
        std = np.std(signal)
        return (signal * std) + mean

    @staticmethod
    def special_vehicle(data):
        x_val, y_val = data

        count = 0
        
        
        greater_than_900 = x_val > 1100
        lower_than_1200 = x_val < 1500
        frequency = np.where(greater_than_900&lower_than_1200)
        if y_val[frequency[0][0]] > 4500:
            count += 1
            if count == 1:
                with open('utils/config.json') as f:
                    config = json.load(f)
                EMERGENCY = config["EMERGENCY"]
                EMERGENCY = 1
                # print(EMERGENCY)

                config["EMERGENCY"] = EMERGENCY

                with open('utils/config.json', 'w') as f:
                    json.dump(config, f)
                count = 0
        else:
            count = 0
            with open('utils/config.json') as f:
                config = json.load(f)
            EMERGENCY = config["EMERGENCY"]
            EMERGENCY = 0
            # print(EMERGENCY)

            config["EMERGENCY"] = EMERGENCY

            with open('utils/config.json', 'w') as f:
                json.dump(config, f)
import cv2
import numpy as np
import multiprocessing as mp
import json
import socket
import pickle
import struct

from utils import audio
from utils.audio import Audio
from utils.traffic_light import Traffic

import importlib
importlib.invalidate_caches()
importlib.reload(audio)
Audio = audio.Audio


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '10.91.41.64'
port = 9999
client_socket.connect((host_ip, port))

def traffic():
    # Traffic.difference()
    cv2.setTrackbarPos("Time", "Input", 60)
    time = 60
    previous_value = 0
    while time >= 0:
        full_msg = ''
        while True:
            msg = client_socket.recv(8)
            if len(msg) <= 0:
                break
            full_msg += msg.decode("utf-8")

        if len(full_msg) > 0:
            print(full_msg)

        difference = full_msg["difference"]
        priority = full_msg["priority"]

        time = Traffic.track_difference()
        current_value = difference
        if current_value == previous_value:
            Traffic.COUNT = 0 #The value doesn't change, adjust the time only by 1 second
        else:
            Traffic.COUNT = 1 #The value has been changed, adjust the time by multiple seconds
        previous_value = current_value
        traffic = Traffic(difference=difference, priority=priority)
        cv2.waitKey(1000)
        time -= 1
        time, color = traffic.traffic_light(time)
        
        with open('utils/config.json') as f:
            config = json.load(f)
        emergency = config["EMERGENCY"]
        if emergency == 1:
            cv2.waitKey(10000)
        cv2.setTrackbarPos("Time", "Input", time)
        # transmission(color)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

client_socket.close()

def special_vehicle():
    Audio.sound_wave()
    

if __name__ == '__main__':
    
    p1 = mp.Process(target=traffic)
    p2 = mp.Process(target=special_vehicle)

    # Start the threads
    p1.start()
    p2.start()

    

# COLOR_1 = Traffic.color1
# COLOR_2 = Traffic.color2
# color = [COLOR_1, COLOR_2]
# transmission(color)

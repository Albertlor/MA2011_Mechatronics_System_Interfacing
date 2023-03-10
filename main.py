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

# difference = 0
# priority = 0

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '10.91.84.87'
    #host_ip = '192.168.0.121'
    #host_ip = '10.91.41.64'
    port = 9999
    client_socket.connect((host_ip, port))
    while True:
        #data = client_socket.recv(1024).decode('utf-8')
        full_msg = ''
        
        msg = client_socket.recv(1024)
        if len(msg) <= 0:
            break
        full_msg = msg.decode("utf-8")
        try:
            dict_data = json.loads(full_msg)
        except ValueError:
            pass
        print(dict_data)
    # difference = int(data[0])
    # priority = int(data[1])
        with open('config2.json') as f:
            try:
                config2 = json.load(f)
            except ValueError:
                pass
        config2['difference'] = dict_data['difference']
        config2['priority'] = dict_data['priority']

        with open('config2.json', 'w') as f:
            json.dump(config2, f)

        cv2.waitKey(1500)
        


def traffic():
    # Traffic.difference()
    
    cv2.setTrackbarPos("Time", "Input", 60)
    time = 60
    previous_value = 0
    while time >= 0:
        try: 
            with open('config2.json') as f:
                try:
                    config2 = json.load(f)
                except ValueError:
                    pass

            difference = config2['difference']
            priority = config2['priority']           

            # print(f'difference: {difference}, priority: {priority}')
            cv2.setTrackbarPos("Difference", "Input", difference)
            cv2.setTrackbarPos("Priority", "Input", priority)
            traffic = Traffic(difference=difference, priority=priority)
            
            _, _, time = Traffic.track_difference()
            cv2.waitKey(1500)
            time -= 1
            time, color = traffic.traffic_light(time)

            current_value = difference
            if current_value == previous_value:
                Traffic.COUNT = 0 #The value doesn't change, adjust the time only by 1 second
            else:
                Traffic.COUNT = 1 #The value has been changed, adjust the time by multiple seconds
            previous_value = current_value
            
            with open('utils/config.json') as f:
                try:
                    config = json.load(f)
                except ValueError:
                    pass
            emergency = config["EMERGENCY"]
            print(f'emergency status: {emergency}')
            if emergency == 1:
                cv2.waitKey(10000)
         
            cv2.setTrackbarPos("Time", "Input", time)

            if time == 0:
                cv2.waitKey(10000)
            # transmission(color)

        except UnboundLocalError:
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# client_socket.close()

def special_vehicle():
    Audio.sound_wave()
    

if __name__ == '__main__':
    
    p1 = mp.Process(target=traffic)
    p2 = mp.Process(target=special_vehicle)
    p3 = mp.Process(target=client)

    # Start the threads
    p1.start()
    p2.start()
    p3.start()

    

# COLOR_1 = Traffic.color1
# COLOR_2 = Traffic.color2
# color = [COLOR_1, COLOR_2]
# transmission(color)

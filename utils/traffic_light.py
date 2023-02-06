import cv2
import matplotlib.pyplot as plt
import time


class Traffic:
    """
    Control the time from red to green or the other way around depends on:
    1. The number difference of vehicles at each junction
    2. Whether there are special vehicles
    """
    T = 10 #Remaining time
    T_0 = 3 #Time adjustment by 3 seconds
    t = T - T_0 #Net remaining time
    
    def __init__(self, difference, priority):
        self.difference = difference
        self.priority = priority

    def red_to_green(self):
        if self.priority == 1:
            if self.difference == 1:
                Traffic.t = Traffic.T - Traffic.T_0
                J1 = [(0, 0, 204), Traffic.t]
            elif self.difference == 2:
                Traffic.t = Traffic.T - Traffic.T_0
                J1 = [(51, 51, 255), Traffic.t]
            elif self.difference == 3:
                J1 = [(204, 204, 255), Traffic.t]  
            elif self.difference == 0:
                J1 = [(204, 204, 255), Traffic.t]
        if self.priority == 2:
            if self.difference == 1:
                color_2 = (0, 0, 204)
            elif self.difference == 2:
                color_2 = (51, 51, 255)
            elif self.difference == 3:
                color_2 = (204, 204, 255)
            elif self.difference == 0:
                pass

    def green_to_red(self):
        pass

    def adjustment(self):


    @staticmethod
    def display_light_component():
        pass


    # def vehicle_num_difference(self):
    #     #should be in the script of object detection
    #     pass

    # def special_vehicle(self):
    #     #should be in the script of audio
    #     pass
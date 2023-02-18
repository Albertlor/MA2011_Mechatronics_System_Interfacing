import cv2
import matplotlib.pyplot as plt
import time
import numpy as np


def empty(a):
    pass

cv2.namedWindow("Input")
cv2.resizeWindow("Input", 420, 120)
cv2.createTrackbar("Difference", "Input", 0, 3, empty)
cv2.createTrackbar("Priority", "Input", 1, 2, empty)
cv2.createTrackbar("Time", "Input", 0, 1000, empty)

class Traffic:
    """
    Control the time from red to green or the other way around depends on:
    1. The number difference of vehicles at each junction
    2. Whether there are special vehicles
    """
    T_0 = 3 #Time adjustment by 3 seconds
    t = 60 #Net remaining time
    COUNT = 0
    
    def __init__(self, difference, priority):
        self.difference = difference
        self.priority = priority

    def traffic_light(self, time):
        if self.priority == 1:
            if self.difference == 1:
                if Traffic.COUNT == 1:
                    Traffic.t = time - Traffic.T_0
                    Traffic.COUNT = 0
                else:
                    Traffic.t = time
                
            elif self.difference == 2:
                if Traffic.COUNT == 1:
                    Traffic.t = time - Traffic.T_0 * 2
                    Traffic.COUNT = 0
                else:
                    Traffic.t = time
                
            elif self.difference == 3:
                if Traffic.COUNT == 1:
                    Traffic.t = time - Traffic.T_0 * 3
                    Traffic.COUNT = 0
                else:
                    Traffic.t = time

            elif self.difference == 0:
                Traffic.t = time

        if self.priority == 2:
            if self.difference == 1:
                if Traffic.COUNT == 1:
                    Traffic.t = time + Traffic.T_0
                    Traffic.COUNT = 0
                else:
                    Traffic.t = time
                
            elif self.difference == 2:
                if Traffic.COUNT == 1:
                    Traffic.t = time + Traffic.T_0 * 2
                    Traffic.COUNT = 0
                else:
                    Traffic.t = time
                
            elif self.difference == 3:
                if Traffic.COUNT == 1:
                    Traffic.t = time + Traffic.T_0 * 3
                    Traffic.COUNT = 0
                else:
                    Traffic.t = time

            elif self.difference == 0:
                Traffic.t = time
                
        """
        Assume that the current scenario is:
            -Junction 1 red light
            -Junciton 2 green light
        
        Therefore, if the priority goes to J1, J1 should turn green faster, vice versa.
        """
        if Traffic.t > 0 and Traffic.t <= 20:
            J1 = [(204, 204, 255), Traffic.t] #red
            J2 = [(153, 255, 204), Traffic.t] #green
            Traffic.display_light_component(J1, J2)
        elif Traffic.t > 20 and Traffic.t <=40:
            J1 = [(51, 51, 255), Traffic.t]
            J2 = [(0, 255, 128), Traffic.t]
            Traffic.display_light_component(J1, J2)
        elif Traffic.t > 40 and Traffic.t <=60:
            J1 = [(0, 0, 204), Traffic.t]
            J2 = [(0, 204, 102), Traffic.t]
            Traffic.display_light_component(J1, J2)

        return [Traffic.t, Traffic.display_light_component(J1, J2)]

    # @staticmethod
    # def empty(a):
    #     pass

    # @staticmethod
    # def difference():
    #     cv2.namedWindow("Input")
    #     cv2.resizeWindow("Input", 420, 120)
    #     cv2.createTrackbar("Difference", "Input", 0, 3, Traffic.empty)
    #     cv2.createTrackbar("Priority", "Input", 1, 2, Traffic.empty)
    #     cv2.createTrackbar("Time", "Input", 0, 70, Traffic.empty)

    @staticmethod
    def track_difference():
        difference = cv2.getTrackbarPos("Difference", "Input")
        priority = cv2.getTrackbarPos("Priority", "Input")
        time = cv2.getTrackbarPos("Time", "Input")
        return [difference, priority, time]

    @staticmethod
    def display_light_component(J1, J2):
        color1 = J1[0]
        color2 = J2[0]

        image1 = np.zeros((300, 300, 3), dtype = np.uint8)
        cv2.rectangle(image1, (0, 0), (300, 300), color1, -1)

        image2 = np.zeros((300, 300, 3), dtype = np.uint8)
        cv2.rectangle(image2, (0, 0), (300, 300), color2, -1)

        stacked = np.concatenate((image1, image2), axis=1)
        cv2.imshow("Junction 1 / Junction 2", stacked)

        return [color1, color2]

    @staticmethod
    def emergency():
        time = 1000
        priority = 1

        return time, priority
        
    # def special_vehicle(self):
    #     #should be in the script of audio
    #     pass

def main():
    Traffic.difference()
    cv2.setTrackbarPos("Time", "Input", 60)
    time = 60
    previous_value = 0
    while time >= 0:
        difference, priority, time = Traffic.track_difference()
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
        cv2.setTrackbarPos("Time", "Input", time)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()
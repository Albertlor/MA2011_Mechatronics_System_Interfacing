import cv2
import numpy as np
from object_detection.object_detection import ObjectDetection
import math
import socket
import pickle
import threading

# Initialize Object Detection
od = ObjectDetection()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP: ', host_ip)
port = 9999
socket_address = (host_ip, port)

server_socket.bind(socket_address)

server_socket.listen(5)
print("LISTENING AT: ", socket_address)


# Initialize count
count1 = 0
count2 = 0
center_points_prev_frame1 = []
center_points_prev_frame2 = []

tracking_objects1 = {}
tracking_objects2 = {}
track_id1 = 1
track_id2 = 1

ans = {}

# def client(ans):
#     data = pickle.dumps(ans)
#     conn.sendall(data)
#     conn.close()


while True:
    client_socket,addr = server_socket.accept()
    print('GOT CONNECTION FROM: ', addr)
    if client_socket:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while(cap.isOpened()):
        ret1, frame = cap.read()
        ret2, frame = cap.read()
        height, width, _ = frame.shape
        print(height, width)
        # Extract region of interest
        roi1 = frame[100: 300, 300:600]
        roi2 = frame[200: 600, 0:300]
        count1 += 1
        count2 += 1
        if not ret1:
            break

        if not ret2:
            break

        # Point current frame
        center_points_cur_frame1 = []
        center_points_cur_frame2 = []

        # Detect objects on roi1
        (class_ids1, scores1, boxes1) = od.detect(roi1)
        for box1 in boxes1:
            (x1, y1, w1, h1) = box1
            cx1 = int((x1 + x1 + w1) / 2)
            cy1 = int((y1 + y1 + h1) / 2)
            center_points_cur_frame1.append((cx1, cy1))
            #print("FRAME N°", count, " ", x, y, w, h)

            # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.rectangle(roi1, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

        # Only at the beginning we compare previous and current frame
        if count1 <= 2:
            for pt1a in center_points_cur_frame1:
                for pt1b in center_points_prev_frame1:
                    distance1 = math.hypot(pt1b[0] - pt1a[0], pt1b[1] - pt1a[1])

                    if distance1 < 20:
                        tracking_objects1[track_id1] = pt1a
                        track_id1 += 1
        else:

            tracking_objects_copy1 = tracking_objects1.copy()
            center_points_cur_frame_copy1 = center_points_cur_frame1.copy()

            for object_id1, pt1b in tracking_objects_copy1.items():
                object_exists1 = False
                for pt1a in center_points_cur_frame_copy1:
                    distance1 = math.hypot(pt1b[0] - pt1a[0], pt1b[1] - pt1a[1])

                    # Update IDs position
                    if distance1 < 20:
                        tracking_objects1[object_id1] = pt1a
                        object_exists1 = True
                        if pt1a in center_points_cur_frame1:
                            center_points_cur_frame1.remove(pt1a)
                        continue

                # Remove IDs lost
                if not object_exists1:
                    tracking_objects1.pop(object_id1)

            # Add new IDs found
            for pt1a in center_points_cur_frame1:
                tracking_objects1[track_id1] = pt1a
                track_id1 += 1

        for object_id1, pt1a in tracking_objects1.items():
            cv2.circle(roi1, pt1a, 5, (0, 0, 255), -1)
            cv2.putText(roi1, "car", (pt1a[0], pt1a[1] - 7), 0, 1, (0, 0, 255), 2)

        print("Tracking objects1")
        print(tracking_objects1)


        print("CUR FRAME LEFT PTS 1")
        print(center_points_cur_frame1)


        # Make a copy of the points
        center_points_prev_frame1 = center_points_cur_frame1.copy()

        # Detect objects on roi2
        (class_ids2, scores2, boxes2) = od.detect(roi2)
        for box2 in boxes2:
            (x2, y2, w2, h2) = box2
            cx2 = int((x2 + x2 + w2) / 2)
            cy2 = int((y2 + y2 + h2) / 2)
            center_points_cur_frame2.append((cx2, cy2))
            # print("FRAME N°", count, " ", x, y, w, h)

            # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.rectangle(roi2, (x2, y2), (x2 + w2, y2 + h2), (0, 255, 0), 2)

        # Only at the beginning we compare previous and current frame
        if count2 <= 2:
            for pt2a in center_points_cur_frame2:
                for pt2b in center_points_prev_frame2:
                    distance2 = math.hypot(pt2b[0] - pt2a[0], pt2b[1] - pt2a[1])

                    if distance2 < 20:
                        tracking_objects2[track_id2] = pt2a
                        track_id2 += 1
        else:

            tracking_objects_copy2 = tracking_objects2.copy()
            center_points_cur_frame_copy2 = center_points_cur_frame2.copy()

            for object_id2, pt2b in tracking_objects_copy2.items():
                object_exists2 = False
                for pt2a in center_points_cur_frame_copy2:
                    distance2 = math.hypot(pt2b[0] - pt2a[0], pt2b[1] - pt2a[1])

                    # Update IDs position
                    if distance2 < 20:
                        tracking_objects2[object_id2] = pt2a
                        object_exists2 = True
                        if pt2a in center_points_cur_frame2:
                            center_points_cur_frame2.remove(pt2a)
                        continue

                # Remove IDs lost
                if not object_exists2:
                    tracking_objects2.pop(object_id2)

            # Add new IDs found
            for pt2a in center_points_cur_frame2:
                tracking_objects2[track_id2] = pt2a
                track_id2 += 1

        for object_id2, pt2a in tracking_objects2.items():
            cv2.circle(roi2, pt2a, 5, (0, 0, 255), -1)
            cv2.putText(roi2, "car", (pt2a[0], pt2a[1] - 7), 0, 1, (0, 0, 255), 2)

        print("Tracking objects2")
        print(tracking_objects2)

        print("CUR FRAME LEFT PTS 2")
        print(center_points_cur_frame2)

        cv2.imshow("Frame", frame)
        cv2.imshow("roi1", roi1)
        cv2.imshow("roi2", roi2)

        # Make a copy of the points
        center_points_prev_frame2 = center_points_cur_frame2.copy()

        def vehicle_num_difference(tracking_objects1, tracking_objects2):
            num = 0
            junction = 0
            if (len(tracking_objects1) > len(tracking_objects2)):
                num = len(tracking_objects1) - len(tracking_objects2)
                junction = 1
            elif (len(tracking_objects2) > len(tracking_objects1)):
                num = len(tracking_objects2) - len(tracking_objects1)
                junction = 2
            else:
                num = 0
                junction = 0

            ans['difference'] = num
            ans['priority'] = junction

            return ans


        answer = vehicle_num_difference(tracking_objects1, tracking_objects2)
        print(answer)
        a = pickle.dumps(answer)
        client_socket.send(a)




        key = cv2.waitKey(1)
        if key == 27:
            client_socket.close()
            break


cap.release()
cv2.destroyAllWindows()

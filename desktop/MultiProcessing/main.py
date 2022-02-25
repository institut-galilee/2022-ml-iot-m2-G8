from datetime import time

import speech_recognition
import threading
import socket
import face_recognition
import cv2
import numpy as np
import os
import time
import sys
from collections import Counter
import tkinter
from tkinter import messagebox
from tkinter import *
video_capture = cv2.VideoCapture(0)
tempsattente = 10
temps_total = 10 * 1
os.system("cls")


def face_recognitions(etats, connex_mode):
    path = 'pictures'

    known_face_encodings = []
    for file in os.listdir(path):
        # Check whether file is an jpg format or not
        if file.endswith(".jpg"):
            file_path = f"{path}/{file}"
            img_file_recog = face_recognition.load_image_file(file_path)
            known_face_encodings.append(face_recognition.face_encodings(img_file_recog)[0])
    known_face_names = [
        "Mehdi",
        "Mohammed",
    ]

    # Initialize some variables
    face_locations = []
    face_names = []
    process_this_frame = True
    t_end = time.time() + tempsattente
    if connex_mode == 1 :
        t_end = time.time() + 10
    total_names = []
    all_frames = 0
    while time.time() < t_end:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            all_frames += 1
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            total_names.append(name)
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break

    # Release handle to the webcam
    occurence_element = []
    returned_name = ""
    error_state = "tb"
    if total_names:
        unique_total_names = np.unique(total_names)
        occurence_count = Counter(total_names)
        returned_name = occurence_count.most_common(1)[0][0]
        for i in range(len(unique_total_names)):
            occurence_element.append(total_names.count(unique_total_names[i]) / len(total_names))
        for i in range(len(unique_total_names)):
            if unique_total_names[i] == returned_name and occurence_element[i] <=0.2:
                error_state = "abs"
            if unique_total_names[i] != returned_name:
                if unique_total_names[i] == "Unknown":
                    if occurence_element[i] >= 0.2:
                        error_state = "unk"
                else:
                    if occurence_element[i] > 0:
                        error_state = "nau"
    if len(total_names) / all_frames < 0.5 :
        error_state = "abs"
    if connex_mode == 1:
        etats[1] = returned_name
        etats[2] = error_state
    else:
        etats[0][2] = error_state


def speech_recognitions(etats):

    recognizer = speech_recognition.Recognizer()
    speech_keywords = ["question", "reponse", "réponse", "réponds", "questions"]
    said_stuff = []
    t_end = time.time() + tempsattente
    while time.time() < t_end:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                text = recognizer.recognize_google(audio, language="fr_FR")
                text = text.lower()
                said_stuff.append(text)
        except:
            continue
    flag5 = 0
    for sentence in said_stuff:
        for keyword in speech_keywords:
            if keyword in sentence:
                flag5 = 1
    etats[0] = flag5


def object_detection(etats):
    detected_object = []
    classFile = 'coco.names'
    with open(classFile, 'rt') as f:
        classNames = (f.read().rstrip('\n').split('\n'))
    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    all_stuff_detected = []
    t_end = time.time() + tempsattente
    while time.time() < t_end:
        success, img = video_capture.read()
        classIds, confs, bbox = net.detect(img, confThreshold=0.5)
        detected_object_i = []
        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                if classId <= 80:
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, classNames[classId - 1], (box[0] + 10, box[1] + 40),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(img, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    detected_object_i.append(classNames[classId-1])
                    all_stuff_detected.append(classNames[classId-1])
        detected_object.append(detected_object_i)

    objects_dectetcetd, number_detected = np.unique(all_stuff_detected,return_counts=True)
    etats[3] = "tb"
    flag_tel = 0
    for i in range(len(objects_dectetcetd)):
        if objects_dectetcetd[i] in ["book"] and \
                number_detected[i] / len(detected_object) >= 0.5:
            etats[3] = "livre"
        if objects_dectetcetd[i] in ["cell phone"]:
            flag_tel = 1
            if (number_detected[i]/len(detected_object) < 0.1):
                etats[3] = "tel1"
            if (number_detected[i]/len(detected_object) >= 1.7):
                etats[3] = "tel2"
        if objects_dectetcetd[i] in ["laptop", "keyboard"] and\
                number_detected[i]/len(detected_object) >= 0.5:
            etats[3] = "pc"
    if flag_tel == 0 and etats[3] == "tb":
        etats[3] = "tel1"

root = Tk()
root.title("The exam App")
root.geometry("400x600")
mylabel1 = Label(root, text="The system is trying to identify you")
mylabel1.pack()
root.update()

etats = [0, "", "tb", "nothing", 0, "nothing"]

flag2 = 0
while flag2 == 0:
    face_recognitions(etats, 1)
    if etats[1] and etats[1] != "Unknown" and etats[2] == "tb":
        flag2 = 1
    else:
        mylabel2 = Label(root, text="The connexion is not established either we could not identify you or someone else is present,"
              " try to be somewhere alone")
        mylabel2.pack()
        root.update()

mylabel = Label(root, text="Bienvenue Mr/Mme : " + etats[1])
mylabel.pack()
root.update()

HOST = '192.168.137.1'
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except socket.error as err:
    print('Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1])
    sys.exit()


s.listen(10)


def listen(phone_id, etats):
    str_phone_id = ''.join([phone_id])
    time_end = time.time() + tempsattente
    all_stuff_detected = []
    detected_object = []
    accelo = 0
    while time.time() < time_end:
        try:
            conn, addr = s.accept()
            received_id = addr[0]
            if str_phone_id == received_id:
                buf = conn.recv(64)
                received_object = buf.decode('ascii').split("|")
                detected_objects = received_object[0].split(",")
                if "Motion" in received_object[1]:
                    accelo += 1
                detected_object_i = []
                for obj in detected_objects :
                    detected_object_i.append(obj)
                    all_stuff_detected.append(obj)
                detected_object.append(detected_object_i)
        except:
            continue
    objects_dectetcetd, number_detected = np.unique(all_stuff_detected, return_counts=True)
    etats[0][5] = "tb"
    for i in range(len(objects_dectetcetd)):
        if objects_dectetcetd[i] in ["book"] and \
                number_detected[i] / len(detected_object) >= 0.1:
            etats[0][5] = "livre"
        elif objects_dectetcetd[i] in ["cell phone"] and \
                number_detected[i] / len(detected_object) >= 0.1:
            etats[0][5] = "tel"
        elif objects_dectetcetd[i] in ["laptop", "keyboard", "tv"] and \
                number_detected[i] / len(detected_object) >= 2:
            etats[0][5] = "pc"
        elif objects_dectetcetd[i] in ["person"] and \
                number_detected[i] / len(detected_object) >= 0.5:
            etats[0][5] = "person"
    etats[0][4] = 0
    if detected_object:
        if accelo / len(detected_object) > 0.5:
            etats[0][4] = 1
    s.close()


def connex_test():
    flag_some = 0
    while 1:
        conn, addr = s.accept()
        buf = conn.recv(64)
        if buf.decode('ascii') == "connexion_established":
            mylabel4 = Label(root, text="The connexion has been established with the phone")
            mylabel4.pack()
            root.update()
            return addr[0]
        if flag_some == 0:
            mylabel5 = Label(root, text="No connection with phone, try closing the app and opening it again.")
            flag_some = 1
            mylabel5.pack()
            root.update()


mylabel6 = Label(root, text="You can enter the mobile app now")
mylabel6.pack()
root.update()
id_phone = connex_test()


time_end = time.time() + temps_total
while time.time() < time_end:
    p1 = threading.Thread(target=speech_recognitions, args=([etats]))
    p4 = threading.Thread(target=listen, args=(id_phone, [etats]))
    p2 = threading.Thread(target=face_recognitions, args=([etats], 0))
    p3 = threading.Thread(target=object_detection, args=[etats])
    p4.start()
    p1.start()
    p1_waiting_time = time.time() + tempsattente
    p2.start()
    p3.start()
    time.sleep(20)
    root.update()
    # Leave
    if etats[2] == "abs" and etats[4] == 1:
        messagebox.showwarning("Warning!!!", "You are trying to leave !")
        root.update()
        break
    # Person detected
    elif etats[2] == 'unk' or etats[2] == 'nau' or (etats[0] == 1 and etats[5] == "person"):
        messagebox.showwarning("Warning!!!", "You are trying to cheat, a non authorized person has been detected")
        root.update()
        break
    # Object detected
    elif etats[5] == "livre" or etats[5] == "tel" or etats[5] == "pc" or etats[3] == 'tel2':
        messagebox.showwarning("Warning!!!", "You are trying to sheet, an non authorized object has been detected")
        root.update()
        break
    # Phone not adjusted
    elif etats[3] == 'tel1':
        messagebox.showwarning("Warning!!!", "Your phone is not adjusted")
        root.update()
        break


video_capture.release()
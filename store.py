import face_recognition
import cv2
import os
import datetime
import pyttsx3
import csv

# Create an object to convert text to speech
txt_sp = pyttsx3.init()
txt_sp.setProperty('rate', 120)

# Initialize last spoken times
last_spoken_time = None
last_spoken_time_u = None

# Load employee encodings from folders
employee_encodings = []
employee_names = []

dirs = os.listdir("DB")



for employee in dirs:
    sub_dir = os.path.join("DB", employee)
    employee_encodings_temp = []
    images=os.listdir(sub_dir)

    for img in images:
        img_path = os.path.join(sub_dir, img)
        image = face_recognition.load_image_file(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_encoding = face_recognition.face_encodings(image)

        if face_encoding:
            encoding = face_encoding[0]
            employee_encodings_temp.append(encoding)

    employee_encodings.append(employee_encodings_temp)
    employee_names.append(employee)

# Start video capture
video = cv2.VideoCapture(0)  # Adjust for camera index

# Define CSV file details
col_names = ["Name", "Time"]

attended_today=set()

previous_name=None

while True:
    success, frame = video.read()

    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = [face_recognition.compare_faces(encodings, face_encoding, tolerance=0.4) for encodings in employee_encodings]

        name = "Unknown"

        for i, match in enumerate(matches):
            if True in match:
                index = match.index(True)
                name = employee_names[i]
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 0, 0), 1)
                break

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        current_time = datetime.datetime.now().time()

        if name == "Unknown":
            if last_spoken_time_u is None or (datetime.datetime.combine(datetime.date.today(), current_time) - last_spoken_time_u).seconds >= 60:
                txt_sp.say("Hi welcome to cyclery..")
                txt_sp.runAndWait()
                last_spoken_time_u = datetime.datetime.combine(datetime.date.today(), current_time)
                name=previous_name

        if name in employee_names:
            if last_spoken_time is None or (datetime.datetime.combine(datetime.date.today(), current_time) - last_spoken_time).seconds >= 3600 or name != previous_name:
                txt_sp.say("Hi " + name + ", Welcome to cyclery")
                txt_sp.runAndWait()
                last_spoken_time = datetime.datetime.combine(datetime.date.today(), current_time)
                previous_name = name
                

        attendance_threshold_time = datetime.time(12, 0)
        if current_time < attendance_threshold_time and name != "Unknown":
            if name not in attended_today:
                txt_sp.say("Attendance taken...")
                txt_sp.runAndWait()
                attended_today.add(name)

                frmt_date = datetime.datetime.now().strftime("%d-%m-%y")
                frmt_time = datetime.datetime.now().strftime("%I:%M %p")
                attendance = [name, str(frmt_time)]

                csv_file_path = "Attendance/attendance_" + frmt_date + ".csv"

                if os.path.isfile(csv_file_path):
                    with open(csv_file_path, "a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(attendance)
                else:
                    with open(csv_file_path, "w", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(col_names)
                        writer.writerow(attendance)

    cv2.imshow('Video', frame)

    k = cv2.waitKey(1)
    if k == ord("q"):
        break

# Release resources
video.release()
cv2.destroyAllWindows()

import cv2
import os
import face_recognition
import datetime
from connection import conn
from flask import Flask, render_template, request, redirect, url_for
import re
import subprocess

app = Flask(__name__)

known_faces = []
known_names = []

today = datetime.date.today().strftime("%d_%m_%Y")

def get_known_encodings():
    global known_faces, known_names
    known_faces = []
    known_names = []
    for filename in os.listdir('static/faces'):
        image = face_recognition.load_image_file(os.path.join('static/faces', filename))
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:
            encoding = face_encodings[0]
            known_faces.append(encoding)
            known_names.append(os.path.splitext(filename)[0])

def totalreg():
    return len(os.listdir('static/faces/'))

def extract_attendance():
    results = conn.read(f"SELECT * FROM {today}")
    return results

def mark_attendance(person):
    name_roll = person.rsplit('_', 1)
    name = name_roll[0]
    roll_no = name_roll[1]
    current_time = datetime.datetime.now().strftime('%H:%M:%S')

    exists = conn.read(f"SELECT * FROM {today} WHERE roll_no = %s", (roll_no,))
    if exists is not None and len(exists) == 0:
        try:
            conn.insert(f"INSERT INTO {today} (name, roll_no, time) VALUES (%s, %s, CURTIME())", (name, roll_no))
            conn.conn.commit()
            print(f"✅ Attendance marked for {name} ({roll_no})")

        except Exception as e:
            print(e)

def identify_person():
    video_capture = cv2.VideoCapture(0)
    attendance_marked = False

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Unable to read from camera.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        face_locations = face_recognition.face_locations(rgb_frame)

        print("Detected face locations:", face_locations)  # Debugging

        face_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=face_locations) if face_locations else []

        recognized_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = 'Unknown'
            if True in matches:
                matched_indices = [i for i, match in enumerate(matches) if match]
                for index in matched_indices:
                    name = known_names[index]
                    recognized_names.append(name)

        if recognized_names:
            for name in recognized_names:
                mark_attendance(name)
            attendance_marked = True

        cv2.imshow('camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or attendance_marked:
            break

    video_capture.release()
    cv2.destroyAllWindows()

@app.route('/')
def home():
    conn.create(f"CREATE TABLE IF NOT EXISTS {today} (name VARCHAR(30), roll_no VARCHAR(20) PRIMARY KEY, time VARCHAR(10))")
    userDetails = extract_attendance()
    get_known_encodings()
    return render_template('home.html', l=len(userDetails), today=today.replace("_", "-"), totalreg=totalreg(),
                           userDetails=userDetails)

@app.route('/video_feed', methods=['GET'])
def video_feed():
    identify_person()
    return redirect(url_for('home'))

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    name = request.form['newusername']
    roll_no = request.form['newrollno']
    phone_no = request.form['phone']
    email = request.form['email']

    userimagefolder = 'static/faces'
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Unable to open camera")
        return redirect(url_for('home'))

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Unable to capture frame")
            break

        flipped_frame = cv2.flip(frame, 1)
        text = "Press Q to Capture & Save the image"
        font = cv2.FONT_HERSHEY_COMPLEX
        font_scale = 0.9
        font_color = (0, 0, 200)
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = (frame.shape[0] - 450)
        cv2.putText(flipped_frame, text, (text_x, text_y), font, font_scale, font_color, thickness, cv2.LINE_AA)

        cv2.imshow('camera', flipped_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            img_name = f"{name}_{roll_no}.jpg"
            cv2.imwrite(os.path.join(userimagefolder, img_name), flipped_frame)
            break

    video_capture.release()
    cv2.destroyAllWindows()

    conn.insert("INSERT INTO contact_details (phone_no, email) VALUES (%s, %s)", (phone_no, email))
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

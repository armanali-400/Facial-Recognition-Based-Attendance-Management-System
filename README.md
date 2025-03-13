# **Facial Recognition-Based Attendance Management System** 🎭✅  

A **Flask-based web application** that uses **Facial Recognition** to automate attendance tracking. This system leverages **OpenCV, Dlib, and Face Recognition** to detect and identify students and record their attendance in a **MySQL database**.  

---

## **🛠 Features**  
✅ **Face Recognition-Based Attendance** – Detects and marks attendance automatically.  
✅ **Web Interface (Flask)** – Simple and user-friendly UI to manage attendance.  
✅ **Real-time Face Detection** – Uses OpenCV to capture live feed from the webcam.  
✅ **MySQL Database Integration** – Stores attendance records securely.  
✅ **User Registration** – Allows new users to be added with face images.  
✅ **Auto-Updating Attendance Table** – Displays today's attendance dynamically.  

---

## **📂 Project Structure**  

```
📁 Facial-Recognition-Attendance
│── 📁 static                # Stores face images
│── 📁 templates             # HTML templates (Flask frontend)
│── 📄 app.py                # Main Flask application
│── 📄 connection.py         # Handles MySQL database connection
│── 📄 appwr.py              # Additional processing for face recognition
│── 📄 requirements.txt      # List of dependencies
│── 📄 README.md             # Project documentation
```

---

## **📦 Installation Guide**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/armanali-400/Facial-Recognition-Based-Attendance-Management-System.git

```

### **2️⃣ Create a Virtual Environment (Optional but Recommended)**  
```bash
python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate      # For Windows
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up MySQL Database**  
1. Open **MySQL Workbench** or **Command Line**  
2. Create a database:  
   ```sql
   CREATE DATABASE attendance;
   ```
3. Update **connection.py** with your MySQL credentials.  

---

## **🚀 Running the Application**  
```bash
python app.py
```
Then, open your browser and go to:  
📌 **http://127.0.0.1:5000/**  

---

## **🛠 Technologies Used**  
🚀 **Flask** - Python web framework  
📸 **OpenCV** - Computer Vision library  
🧠 **Dlib** - Machine learning toolkit  
🎭 **Face Recognition** - Deep learning-based facial recognition  
💾 **MySQL** - Database management system  
🖥 **HTML, CSS, Bootstrap** - Frontend  

---

## **📜 License**  
This project is **open-source** and available and free to use.

---

✨ Author
Your Arman Ali
https://github.com/armanali-400 |  linkedin.com/in/armana002 
  

---

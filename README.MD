# FaceRecognization-Register

A robust and user-friendly face registration and recognition system using Python and HTML, designed for real-time user enrollment and identification. The project features both a command-line interface and a modern web frontend, making it suitable for various access control, attendance, or authentication scenarios.

---

## Features

- **Face Registration:**  
  Register new users by capturing their faces via webcam, saving encodings and user information for future recognition. Multiple angles/attempts can be registered for improved accuracy.

- **Face Recognition:**  
  Real-time recognition via webcam or web interface, identifying registered users and displaying their names.

- **User Management:**  
  List all registered users with IDs and timestamps. System statistics show the number of registered faces, stored images, and database entries.

- **System Status & Testing:**  
  Built-in checks for dependencies, file consistency, backend connection, and data health. Includes test modes for recognition and backend API endpoints.

- **Multiple Interfaces:**  
  - **Command-Line Interface:** Interactive menu in `main.py` for registration, recognition, user listing, stats, and system tests.
  - **Web Frontend:** Clean UI in `index.html` for registration and recognition, with live video, status, and user controls.

- **Extensive Feedback & Robustness:**  
  Color-coded messages, error handling, and user instructions enhance usability.

---

## Demo

![FaceRecognization-Register Screenshot](assets/screenshot.png)

*Replace the above with your own screenshot after running the app!*

---

## Getting Started

### Prerequisites

- Python 3.7+
- Webcam
- [pip](https://pip.pypa.io/en/stable/)
- (For web frontend) Modern web browser

---

## Setup Instructions (on a New Device)

1. **Clone the repo or copy the project folder to your new device:**
   ```bash
   git clone https://github.com/shirsenduda/FaceRecognization-Register.git
   cd FaceRecognization-Register
   ```
   *Or copy the folder via USB, cloud, or other means.*

2. **Install Python (if not installed):**
   - Download and install Python from [python.org](https://www.python.org/downloads/).
   - Ensure `pip` is available (comes by default with recent Python versions).

3. **Install dependencies:**
   - Open a terminal or command prompt in the project folder.
   - Run the automated installer:
     ```bash
     python install.py
     ```
     *This will install all required Python libraries, create necessary folders, and test your environment.*

   - **OR** manually install requirements:
     ```bash
     pip install -r requirements.txt
     ```

4. **Connect a webcam** if you want to use the camera-based features.

5. **Run the application:**
   - **Command-line interface:**  
     ```bash
     python main.py
     ```
   - **Web backend (for using the web UI):**  
     ```bash
     python app.py
     ```
   - **Graphical interface (optional):**  
     ```bash
     python fixed_gui_app.py
     ```

6. **Using the web interface:**
   - Open `index.html` in your browser.
   - Make sure the backend (`app.py`) is running and accessible (usually at `http://localhost:5000`).
   - Register faces and test recognition directly from the browser.

7. **(Optional) Configuration:**
   - Edit `config.ini` to adjust recognition parameters if needed.
   - Review `requirements.txt` for library versions.

---

## Usage

### CLI Menu

```
1. 👤 Register New Face
2. 🔍 Start Face Recognition
3. 👥 List Registered Users
4. 🧪 Test Recognition System
5. 📊 View System Status
6. 🚪 Exit
```

### Web UI

- **Register:** Enter your name, start registration, and capture your face.
- **Recognize:** Start recognition to identify faces in real time.
- **List Users & Check Status:** View registered users and backend status.

---

## Configuration & Tips

- **Edit `config.ini`** to adjust recognition parameters.
- **`requirements.txt`** lists all Python dependencies.
- Ensure good lighting and clear camera view for best results.
- Register multiple angles for each face for higher accuracy.

---

## Tech Stack

- **Python:** OpenCV, face_recognition, pandas, numpy, colorama, Flask, etc.
- **HTML/CSS/JS:** For the web interface.
- **Data Storage:** Pickle files, Excel, and image folders.

---

## System Status & Stats

- Number of registered faces, images, and database entries.
- Consistency check between encodings, images, and database.
- Backend API health checks and diagnostics.

---

## License

MIT

---

## Author

shirsenduda

---

*For issues, suggestions, or contributions, please open an issue or PR on GitHub!*
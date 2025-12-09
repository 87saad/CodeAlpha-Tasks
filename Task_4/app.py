import os
from flask import Flask, render_template, Response, request, jsonify
import cv2
from ultralytics import YOLO

app = Flask(__name__)

model = YOLO('yolov8n.pt')
video_source = 0  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_video', methods=['POST'])
def upload_video():
    global video_source
    if 'video' not in request.files:
        return jsonify({"success": False, "error": "No file"}), 400
    
    file = request.files['video']
    file_path = os.path.join("static", "temp_video.mp4")
    file.save(file_path)
    
    video_source = file_path  
    return jsonify({"success": True})

def generate_frames():
    global video_source
    cap = cv2.VideoCapture(video_source)  
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        results = model.track(frame, persist=True)
        annotated_frame = results[0].plot() 

        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reset_webcam', methods=['POST'])
def reset_webcam():
    global video_source
    video_source = 0
    return jsonify({"success": True})

if __name__ == "__main__":
    if not os.path.exists('static'): os.makedirs('static')
    app.run(debug=True)
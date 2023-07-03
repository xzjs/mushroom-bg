from flask import Flask, Response
import cv2

app = Flask(__name__)


@app.route("/api/camera")
def camera():
    cap = cv2.VideoCapture(6)
    _, frame = cap.read()
    frame = cv2.imencode('.jpg', frame)[1].tobytes()
    cap.release()
    content = (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(content,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

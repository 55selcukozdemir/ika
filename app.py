from flask import Flask, render_template, Response, request
import setup_db as db
import cv2
from requests import request
import numpy as np


app = Flask(__name__,static_url_path="/static")

# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

camera = cv2.VideoCapture("static/images/segmentation.jpg")  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # result = model(frame)

            # ims = np.squeeze(result.render())
            

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')



@app.route('/segment', methods = ['POST', 'GET'])
def segmetParameter():
    try:
        if request.method == 'POST':
            lower_h =  request.form.get("lower-h")
            lower_s =  request.form.get("lower-h")
            lower_v =  request.form.get("lower-h")

            upper_h =  request.form.get("upper-h")
            upper_s =  request.form.get("upper-h")
            upper_v =  request.form.get("upper-h")
            

            return index()

    except: 
        return index()

if __name__ == '__main__':
    app.run(debug=True)
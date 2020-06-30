# eye_shine
Shine stuff into one's eye...

# Pi details
Prob should not share with internet but...

    Username: pi
    Password: *myName*

IN ORDER FOR THIS TO WORK
Needs a power source of 5.1volts with 3 amps
Need that much power for the servos
    

# Other faster ideas
hogFaceDetector = dlib.get_frontal_face_detector()

faceRects = hogFaceDetector(frameDlibHogSmall, 0)

for faceRect in faceRects:

    x1 = faceRect.left()
    y1 = faceRect.top()
    x2 = faceRect.right()
    y2 = faceRect.bottom()

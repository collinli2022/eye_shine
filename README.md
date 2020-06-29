# eye_shine
Shine stuff into one's eye...

# Pi details
Prob should not share with internet but...
    Username: pi
    Password: *myName*
    

# Other faster ideas
hogFaceDetector = dlib.get_frontal_face_detector()

faceRects = hogFaceDetector(frameDlibHogSmall, 0)

for faceRect in faceRects:

    x1 = faceRect.left()
    y1 = faceRect.top()
    x2 = faceRect.right()
    y2 = faceRect.bottom()

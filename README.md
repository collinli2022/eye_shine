# eye_shine
Shine stuff into one's eye...

# Pi details
Prob should not share with internet but...

    Username: pi
    Password: *myName*

IN ORDER FOR THIS TO WORK
Needs a power source of 5.1volts with 3 amps
Need that much power for the servos

# Order
Camera at middle (white) line at 6.5 inches up
Servo is to the right (me) or left of camera pointing at me 2 inches from the midline
Based on my camera and servo

	my Right 124 deg (bottom servo); x-axis : 40 pixel
	my Left 75 deg (bottom servo); x-axis : 550 pixel
	height 117 deg (top servo); y-axis : 100
    

# Other faster ideas
hogFaceDetector = dlib.get_frontal_face_detector()

faceRects = hogFaceDetector(frameDlibHogSmall, 0)

for faceRect in faceRects:

    x1 = faceRect.left()
    y1 = faceRect.top()
    x2 = faceRect.right()
    y2 = faceRect.bottom()

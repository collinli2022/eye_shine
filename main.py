import cv2
import time
import sys
import servo_control

# Format is bottom, top
pins = [38, 37] # put the pins in here BASED ON THE BOARD
source = 0
showDetails = True

def detectFaceOpenCVHaar(faceCascade, frame, inHeight=250, inWidth=0):
    frameOpenCVHaar = frame.copy()
    frameHeight = frameOpenCVHaar.shape[0]
    frameWidth = frameOpenCVHaar.shape[1]

    if not inHeight:
        inHeight = frameHeight

    if not inWidth:
        inWidth = int((frameWidth / frameHeight) * inHeight)

    scaleHeight = frameHeight / inHeight
    scaleWidth = frameWidth / inWidth

    frameOpenCVHaarSmall = cv2.resize(frameOpenCVHaar, (inWidth, inHeight))
    frameGray = cv2.cvtColor(frameOpenCVHaarSmall, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(frameGray)
    bboxes = []
    for (x, y, w, h) in faces:
        x1 = x
        y1 = y
        x2 = x + w
        y2 = y + h
        cvRect = [int(x1 * scaleWidth), int(y1 * scaleHeight),
                  int(x2 * scaleWidth), int(y2 * scaleHeight),
                  int(w * scaleWidth), int(h * scaleHeight), 
                  int(frameWidth), int(frameHeight)]
        bboxes.append(cvRect)
        cv2.rectangle(frameOpenCVHaar, (cvRect[0], cvRect[1]), (cvRect[2], cvRect[3]), (0, 255, 0),
                      round(frameHeight / 150), 4)

        # Draw eye
        aa = (cvRect[0], cvRect[1])
        bb = (int(cvRect[0] + cvRect[-4]/2.8), int(cvRect[1] + cvRect[-3]/2.8))
        cv2.rectangle(frameOpenCVHaar,aa,bb,(255,0,0),2)

    return frameOpenCVHaar, bboxes

def detectFaceOpenCVHaarfaster(faceCascade, frame, inHeight=300, inWidth=0):
    frameOpenCVHaar = frame.copy()
    frameHeight = frameOpenCVHaar.shape[0]
    frameWidth = frameOpenCVHaar.shape[1]
    if not inWidth:
        inWidth = int((frameWidth / frameHeight) * inHeight)

    scaleHeight = frameHeight / inHeight
    scaleWidth = frameWidth / inWidth

    frameOpenCVHaarSmall = cv2.resize(frameOpenCVHaar, (inWidth, inHeight))
    frameGray = cv2.cvtColor(frameOpenCVHaarSmall, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(frameGray)
    bboxes = []
    for (x, y, w, h) in faces:
        x1 = x
        y1 = y
        x2 = x + w
        y2 = y + h
        cvRect = [int(x1 * scaleWidth), int(y1 * scaleHeight),
                  int(x2 * scaleWidth), int(y2 * scaleHeight),
                  int(w * scaleWidth), int(h * scaleHeight)]
        bboxes.append(cvRect)
    return bboxes

def manipulateServo(boxes, servos):
    x1 = boxes[0]
    y1 = boxes[1]
    x2 = boxes[2]
    y2 = boxes[3]
    w = boxes[4]
    h = boxes[5]
    middleX = boxes[6]/2
    middleY = boxes[7]/2

    x = x1 + w/2.8
    y = y1 + h/2.8

    '''

    my Right 124 deg (bottom servo); x-axis : 40 pixel
    my Left 75 deg (bottom servo); x-axis : 560 pixel
    height 117 deg (top servo); y-axis : 100

    '''

    servos[1].angle(117)
    if(x < middleX):
        print("My Right")
        servos[0].angle(124)
    else:
        print("My Left")
        servos[0].angle(75)

    return [x, y]

    '''
    aa = (int(x1),int(y1))
    bb = (int(x1+w/2.8),int(y1+h/2.8))
    # img = cv2.rectangle(img,aa,bb,(255,0,0),2)

    xx = w-bb[0]
    yy = bb[1]-h

    print(xx/w)
    servos[0].angle( xx/w )
    '''




if __name__ == "__main__" :

    bam = [] # Store servo classes
    # Get Servo Classes
    for i in pins:
        bam.append( servo_control.servoControl(i) )

    bam[0].angle(90)
    bam[1].angle(90)


    faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(source)
    hasFrame, frame = cap.read()
    
    if(showDetails): # show frame + other stuff

        vid_writer = cv2.VideoWriter('output-dnn-{}.avi'.format(str(source).split(".")[0]),cv2.VideoWriter_fourcc('M','J','P','G'), 15, (frame.shape[1],frame.shape[0]))

        frame_count = 0
        tt_opencvHaar = 0

        while(1):
            hasFrame, frame = cap.read()
            if not hasFrame:
                break
            frame_count += 1

            t = time.time()
            outOpencvHaar, bboxes = detectFaceOpenCVHaar(faceCascade, frame)

            x = 0
            y = 0

            if(len(bboxes) != 0):
                bboxes = bboxes[0]
                x, y = manipulateServo(bboxes, bam)

            tt_opencvHaar += time.time() - t
            fpsOpencvHaar = frame_count / tt_opencvHaar

            label = str(x) + " " + str(y) + " ; FPS : {:.2f}".format(fpsOpencvHaar)
            cv2.putText(outOpencvHaar, label, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.imshow("Face Detection Comparison", outOpencvHaar)

            vid_writer.write(outOpencvHaar)
            if frame_count == 1:
                tt_opencvHaar = 0

            k = cv2.waitKey(10)
            if k == 27:
                vid_writer.release()
                break


    else: # used when no monitor/output

        # Comment out
        frame_count = 0
        tt_opencvHaar = 0

        while(1):
            hasFrame, frame = cap.read()
            if not hasFrame:
                break

            # Comment out
            frame_count += 1 
            t = time.time()

            bboxes = detectFaceOpenCVHaarfaster(faceCascade, frame) 
            if(len(bboxes) != 0):
                bboxes = bboxes[0] # want only 1 face
                #manipulateServo(bboxes, bam)

            # Comment out
            tt_opencvHaar += time.time() - t
            fpsOpencvHaar = frame_count / tt_opencvHaar
            label = "FPS: {:.2f}".format(fpsOpencvHaar)
            print(label)

            # Comment out
            if frame_count == 1:
                tt_opencvHaar = 0

            k = cv2.waitKey(10)
            if k == 27:
                break
    
    cv2.destroyAllWindows()
    
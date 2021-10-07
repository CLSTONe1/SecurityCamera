import cv2
import time
import datetime

#Videoキャプチャ（）内はカメラ
cap = cv2.VideoCapture(0)

#顔のデータ読み込み
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")

#検出
detection = False
#検出時刻
detection_stopped_time = None
#タイマースタート
timer_started = False

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
SECONDS_TO_RECORD_AFTER_DETECTION = 5

#読み込み
while True:
    _, frame = cap.read()

    #顔を認識
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-$S") 
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20.0, frame_size)
            print("Started recording")

    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print("Stop Recording")

        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)


    #for (x, y, width, height) in faces:
    #    cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()
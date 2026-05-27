import cv2
import serial
import time
from cvzone.HandTrackingModule import HandDetector

arduino = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8)

ultimo_envio = -1

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        count = fingers.count(1)

        # só aceita 1, 2 ou 3
        if count in [1, 2, 3] and count != ultimo_envio:
            print("Enviando:", count)
            arduino.write(str(count).encode())
            ultimo_envio = count

            cv2.putText(img, f"LED {count}", (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2,
                        (0, 255, 0), 3)

        # opcional: se quiser apagar tudo
        elif count not in [1,2,3]:
            arduino.write(b'0')
            ultimo_envio = 0

    cv2.imshow("Hand LED Control", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
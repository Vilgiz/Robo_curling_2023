import cv2

cap = cv2.VideoCapture(1)  # открываем камеру

cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # выключаем автофокус
cap.set(cv2.CAP_PROP_FOCUS, 50)  # устанавливаем фокус на 50 см

while True:
    ret, frame = cap.read()  # захватываем кадр
    cv2.imshow('frame', frame)  # отображаем кадр
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # ждем нажатия клавиши 'q'
        break
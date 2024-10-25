import cv2

# Replace with your video file path
cap = cv2.VideoCapture('C:/Users/GAGANKUMAR/OneDrive/Desktop/Infosys/Task2/demo/sample.avi')

if not cap.isOpened():
    print("Error: Could not open the video file.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    cv2.imshow('Video Player', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

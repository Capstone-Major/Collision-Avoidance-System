# Importing Required Libraries
from ultralytics import YOLO
import cv2
from detectRegion import decideRegion
import serial
import threading

# Function to send data Serially


def sendDataSerially(transData):
    try:
        ser.write(bytes(transData, "utf-8"))
    except Exception as e:
        print(e)

# Function to make list of points and raw data to send Over Serially


def sendMessage(boxes, points, width):
    global counter, sendData
    regionPoints = decideRegion(boxes, points, width)
    print(regionPoints)

    # if len(regionPoints) == 1:
    #     sendData[regionPoints[0]-1] = 1
    # elif len(regionPoints) > 1:
    #     if regionPoints[1]-regionPoints[0] < 2:
    #         for i in range(regionPoints[0], regionPoints[1]+1):
    #             sendData[i-1] = 1
    #     else:
    #         sendData[4] = 150

    if len(regionPoints) == 4:
        sendData[4] = 150

    else:
        for i in regionPoints:
            sendData[i-1] = 1

    # if counter == 20:
    sendString = f"{sendData[0]},{sendData[1]},{sendData[2]},{sendData[3]},{sendData[4]}\n"
    sendDataSerially(sendString)
    # counter=0
    print(sendData)

    sendData = [0, 0, 0, 0, 110]


# Function to Draw 3 partition Line to divide frame into 4 equal frames
def draw_lines(frame):
    # Get frame dimensions
    height, width, _ = frame.shape

    # Calculate vertical and horizontal positions for lines
    first = 0
    second = (width//2)//2
    third = width//2
    fourth = (width//2+(width//2)//2)
    fifth = width

    # Draw vertical lines
    cv2.line(frame, (first, 0), (first, height), (0, 255, 0), 2)
    cv2.line(frame, (second, 0), (second, height), (0, 255, 0), 2)
    cv2.line(frame, (third, 0), (third, height), (0, 255, 0), 2)
    cv2.line(frame, (fourth, 0), (fourth, height), (0, 255, 0), 2)
    cv2.line(frame, (fifth, 0), (fifth, height), (0, 255, 0), 2)

    return first, second, third, fourth, fifth


# Main function which identify the camera frame and detect car
def main():
    global counter, sendData

    # Load a model
    model = YOLO('yolov8ss.pt')  # pretrained YOLOv8n model

    ret = True
    cap = cv2.VideoCapture(1)

    while ret:
        ret, frame = cap.read()
        first, second, third, fourth, fifth = draw_lines(frame)
        print(first, second, third, fourth, fifth)

        results = model(frame)
        # count = len(results)
        # prediction = results[0].boxes.data.tolist()
        # boxes = results[0].boxes
        boxes = results[0].boxes.data.tolist()
        # print("No of vehicles detected")
        print("CAAAARR", len(boxes))

        # if count>1:
        #     sendDataSerially("0,0,0,0,150\n")
        # else:

        # if len(prediction) > 0:
        #     index = prediction[0][-1]
        if len(boxes) > 0:

            # if (index == 1 or index == 2 or index == 3 or index == 5):
            finBoxes = []
            for i in boxes:
                index = i[-1]
                if (index == 1 or index == 2 or index == 3 or index == 5):
                    x1, y1, x2, y2 = i[0], i[1], i[2], i[3]
                    # counter+=1
                    # cv2.circle(frame, (int(x1), int(y1)), radius=10,
                    #            color=(0, 0, 255), thickness=-1)
                    # cv2.circle(frame, (int(x2), int(y2)), radius=10,
                    #            color=(0, 0, 255), thickness=-1)
                    frame = cv2.rectangle(frame, (int(x1), int(y1)), (int(
                        x2), int(y2)), (0, 255, 0), 2)  # Draw the bounding box
                    finBoxes.append([x1, x2])

            sendMessage(finBoxes, [first, second, third,
                        fourth, fifth], frame.shape[1])
            # inserting text on video
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(frame, "PRESS 'Q' TO EXIT", (40, 40),font, 1, (0, 255, 255), 2,  cv2.LINE_4)

            print("Car detected")
        # else:
        #     print("Car not detected")
        #     sendDataSerially("0,0,0,0,110\n")
        else:
            print("Car not detected")
            sendDataSerially("0,0,0,0,110\n")

        cv2.imshow("Frames", frame)
        if (cv2.waitKey(25) & 0xff == ord('q')):
            break

    cv2.destroyAllWindows()


# Python Main function4
if __name__ == "__main__":
    counter = 0
    sendData = [0, 0, 0, 0, 110]
    ser = serial.Serial(port='COM12', baudrate=115200,)
    main()

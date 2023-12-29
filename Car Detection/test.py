from detectRegion import decideRegion
import serial

def sendDataSerially(transData):
    try:
        ser.write(bytes(transData, "utf-8"))
    except Exception as e:
        print(e)


counter =0
sendData = [0,0,0,0,90]
ser = serial.Serial(port='COM4',baudrate=115200,)
while True:
    x1 = int(input("Enter number first :: "))
    x2 = int(input("Enter second number :: "))

    regionPoints = decideRegion(x1,x2,[0,10,20,30,40])
    print(regionPoints)

    if len(regionPoints)==1:
        sendData[regionPoints[0]-1]=1
    elif len(regionPoints)>1:
        if regionPoints[1]-regionPoints[0] < 2:
            for i in range(regionPoints[0],regionPoints[1]+1):
                sendData[i-1]=1
        else:
            sendData[4]=0

    sendString = f"{sendData[0]},{sendData[1]},{sendData[2]},{sendData[3]},{sendData[4]}\n"
    sendDataSerially(sendString)
    print(sendData)
    sendData=[0,0,0,0,90]
import serial.tools.list_ports
import time

DataSerial = serial.Serial('COM20', 9600)

time.sleep(1)

def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    #Phan nay dua len dashboard
    # try:
    #     if splitData[1] == "TEMP1":
    #         client.publish("bbc-temp-1", splitData[2])
    #
    #     elif splitData[1] == "HUMI1":
    #         client.publish("bbc-humi-1", splitData[2])
    #     elif splitData[1] == "TEMP2":
    #         client.publish("bbc-temp-2", splitData[2])
    #     elif splitData[1] == "HUMI2":
    #         client.publish("bbc-humi-2", splitData[2])
    # except:
    #     pass


while True:
    while DataSerial.inWaiting() == 0:
        pass

    data = DataSerial.readline()
    print(data)
import serial.tools.list_ports
import time
import bytes, re, json

DataSerial = serial.Serial('COM3', 9600)

time.sleep(1)
def jsonify_packet(packet:bytes):
  packet = packet.decode('ascii')
  data = re.findall(r'(?:!TEMP)(.+?)(?::)(.+?)(?:#!HUMI)(?:.*:)(.+?)(?:#!SOLAR)(?:.*:)(.+?)(?:#|#!|$)', packet)

  data = [ {
    "device": x[0],
    "latlon": [10.41115, 106.95474],
    "temp": x[1],
    "humi": x[2],
    "lux": x[3],
  } for x in data ]

  return data

# data = jsonify_packet(b'!TEMP1:30.00#!HUMI1:76.00#!SOLAR1:4.73#\r\n!TEMP2:0.00#!HUMI2:0.00#!SOLAR2:4.98#')
# data = jsonify_packet(dataR)

# def processData(data):
#     data = data.replace("!", "")
#     data = data.replace("#", "")
#     splitData = data.split(":")
#     print(splitData)
#     #Phan nay dua len dashboard
#     # try:
#     #     if splitData[1] == "TEMP1":
#     #         client.publish("bbc-temp-1", splitData[2])
#     #
#     #     elif splitData[1] == "HUMI1":
#     #         client.publish("bbc-humi-1", splitData[2])
#     #     elif splitData[1] == "TEMP2":
#     #         client.publish("bbc-temp-2", splitData[2])
#     #     elif splitData[1] == "HUMI2":
#     #         client.publish("bbc-humi-2", splitData[2])
#     # except:
#     #     pass


while True:
    while DataSerial.inWaiting() == 0:
        pass
    dataR = DataSerial.readline()
    data = jsonify_packet(dataR)
    for x in data:
      print(x)
    # print(data)
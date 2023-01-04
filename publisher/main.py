import json
import random
import time
import bytes, re, json
import serial.tools.list_ports

from paho.mqtt import client as mqtt_client


broker = 'broker.hivemq.com'
port = 1883
topic = "sensors"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

#Lấy dữ liệu từ gateway
DataSerial = serial.Serial('COM3', 9600)
time.sleep(1)

#Xử lý dữ liệu
def jsonify_packet(packet:bytes):
  packet = packet.decode('ascii')
  data = re.findall(r'(?:!TEMP)(.+?)(?::)(.+?)(?:#!HUMI)(?:.*:)(.+?)(?:#!SOLAR)(?:.*:)(.+?)(?:#|#!|$)', packet)

  data = [ {
    "device": x[0],
    # "device": client_id,
    "latlon": [10.41115, 106.95474],
    "temp": x[1],
    "humi": x[2],
    "lux": x[3],
  } for x in data ]

  return data


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        #Đọc du lieu tu cong
        dataR = DataSerial.readline()
        data = jsonify_packet(dataR)

        # data = {
        #     # "device": client_id,
        #     # "latlon": [10.41115, 106.95474],
        #     # "sent" : msg_count,
        #     # "temp": random.randint(290, 320) / 10.0,
        #     # "humi": random.randint(60, 100),
        #     # "lux": random.randint(800, 1500) / 10.0,
        # }
        for x in data:
          msg = f"{json.dumps(x)}"
          result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()

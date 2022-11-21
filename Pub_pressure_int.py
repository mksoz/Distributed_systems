# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
topic = "plane/pressure/internal"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)  #1
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    client.publish("plane/pressure", "RETAIN", retain=True)
    client.will_set("plane/pressure", payload="ERROR CRASH", retain=True)

    def fttomb(ft):
        mb = 1013 - (ft / 27)
        return mb

    while True:
        msg_count += 1

        msg = f"messages: {msg_count}"
        pressure_inside = [0, -150, -350, -500, -500, -500,
                            -100, 200, 600, 1000, 1750, 2700, 4000, 4000, 4000, 4000, 4590, 5200, 6300, 7100,
                            8000,
                            8000, 8000, 8000, 8000, 8000, 8000, 8000, 8000, 8000, 8000,
                            7500, 7100, 6700, 6500, 6500, 6500,
                            6050, 5610, 4960, 4020, 3480, 2940, 2500, 2050, 1510, 950, 540, 0,
                            -500, -350, -200, -100, 0]

        while msg_count < 60:
            time.sleep(1)

            client.publish("plane/pressure/internal", pressure_inside[msg_count])

            msg_count += 1
            #result = client.publish(topic, msg)


        client.disconnect()
"""
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` kPa to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        """

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()



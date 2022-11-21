# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
topic = "plane/pressure"
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
    while True:
        pilot = random.randrange(1, 3)
        stime = random.randrange(5, 10)
        time.sleep(stime)
        msg = f"messages: {msg_count}"

        topic2 = "plane/service/pilot" + str(pilot)
        print(topic2)
        result = client.publish(topic2, "assistance", qos=1)
        #self, topic, payload = None, qos = 0, retain = False, properties = None
        #result = client.publish(topic, msg)


        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` kPa to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()


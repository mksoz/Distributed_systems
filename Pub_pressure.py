# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
topic = "plane/pressure/external"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'


pressure_outside = [0, 0, 0, 0, 0, 0, 1001, #TAKE-OFF
                    1428, 2857, 4285, 5714, 7142, 8571, 10000, 10000, 10000, 10000, 15790, 21600, 27400, 33200,33201, #CLIMB
                    39000, 39000, 39000, 39000, 39000, #CRUISE
                    36000, 31000, 30000, 29999,
                    27850, 23560, 10710, 8560, 6420, 2140, 1000, 800, 600, 400, 360, 250,200,150,100, 50,#DECENT
                    0, 0, 0, 0, 0]#GROUND

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def pub_control(client, msg):
    topic = "plane/control"
    client.publish(topic, msg, qos=1)


def pub_tcp(client, msg):
    topic = "plane/service"
    client.publish(topic, msg)


def pub_Pilot(client, topic, msg, retain=False):

    if retain:
        client.publish(topic, msg, retain=True)
        client.will_set(topic, payload="ERROR CRASH", retain=True)

    client.publish(topic, msg)


def run():
    # first message from control tower
    client_control = connect_mqtt()
    pub_control(client_control, "runway clear for takeoff")
    client_control.disconnect()

    time.sleep(3)

    HIGH = 'TAKE_OFF'
    client_pilot = connect_mqtt()
    #client.loop_start()
    for press in pressure_outside:
        time.sleep(2)
        pub_Pilot(client_pilot, "plane/pressure/external", press)
        if HIGH == 'TAKE_OFF':
                if press > 1000:
                    HIGH = 'CLIMB'
                    print('START CLIMB')
                    continue
                HIGH = 'TAKE_OFF'
                print('TAKING-OFF')
                continue
        else:
            if HIGH == 'CLIMB':
                if press > 33200:
                    HIGH = 'CRUISE'
                    print('START CRUISE')
                    print('Available plane service')
                    print('Automatic plane control')
                    client_pilot.disconnect()
                    continue
                HIGH = 'CLIMB'
                print('CLIMBING')
                continue
            else:
                if HIGH == 'CRUISE':
                    if press == 39000:

                        client_pilot = connect_mqtt()
                        pub_Pilot(client_pilot, "plane/pressure/external", press)
                        client_pilot.disconnect()

                        client_tcp = connect_mqtt()
                        # press service buttons
                        yes = input('Press for calling personal assistance (yes:y)')
                        if yes.lower() == "y":
                            pub_tcp(client_tcp, "Service alert")

                        yes = input('Press for pilot calling (yes:y)')
                        if yes.lower() == "y":
                            pub_tcp(client_tcp, "Pilot alert")
                        client_tcp.disconnect()

                        HIGH = 'CRUISE'
                        continue
                    else:
                        client_pilot = connect_mqtt()
                        HIGH = 'DECENT'
                        print('START DECENT')
                        print('Unavailable plane service')
                        print('Manual plane control')
                        continue
                else:
                    if HIGH == 'DECENT':
                        HIGH = 'DECENT'
                        if press < 1000:
                            pub_Pilot(client_pilot, "plane/control/status", "OK", retain=True)
                            continue
                        if press < 260:
                            HIGH = 'GROUND'
                            print('START GROUND')
                        print('DESCENDING')
                        continue
                    else:
                        if HIGH == 'GROUND':
                            if press > 150:
                                client_control = connect_mqtt()
                                pub_Pilot(client_control,"plane/pilot" ,"Landing in runway 5")
                                client_control.disconnect()
                            HIGH = 'GROUND'
                            print('GROUNDED')
                            continue
    print('STOPED')
    client_pilot.disconnect()

if __name__ == '__main__':
    run()



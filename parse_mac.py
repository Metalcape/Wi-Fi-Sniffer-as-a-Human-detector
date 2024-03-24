import paho.mqtt.client as mqtt
import json
import csv

def is_modified_mac(mac_address : bytearray):
    return ((mac_address[0] & 0b00000010) >> 1) == 1

def mac_to_bytes(mac_address : str):
    return bytearray.fromhex(mac_address.replace(':', ''))

def get_mac_vendor(mac_string : str):
    oui = mac_string[:8].replace(':', '').upper()
    with open('oui.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if oui == row[1]:
                return row[2]
    return "Unknown"

def on_message(client, userdata, message):
    data = json.loads(message.payload.decode("utf-8"))
    for address in data['MAC']:
        mac_bytes = mac_to_bytes(address)
        is_modified = is_modified_mac(mac_bytes)
        vendor = get_mac_vendor(address) if not is_modified else '-'
        print(f"MAC: {address} {'(Modified)' if is_modified else '(Not modified)'} - Vendor: {vendor}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.connect("server.home.arpa")
client.subscribe("Sniffer/#")
client.loop_forever()
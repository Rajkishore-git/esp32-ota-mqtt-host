import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"
port = 1883
topic = "esp32/ota/update"
firmware_url = "http://YOUR_PUBLIC_IP_OR_DOMAIN:8000/latest_firmware.bin"

client = mqtt.Client()
client.connect(broker, port, 60)
client.publish(topic, firmware_url)
client.disconnect()

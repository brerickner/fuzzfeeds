import httplib, urllib
import time
from GPS_API import *
import serial


ser = serial.Serial("/dev/ttyAMA0")  # Pi Serial Port
ser.baudrate = 9600  # Baud rate
ser.timeout = 0.5
sleep = 2 # Seconds to sleep between posts to the channel

key = 'XXXXXXXXXXXXXXXX'  # Thingspeak Write API Key
msgdata = Message() # Message Instance
 
# This Function will upload Latitude and Longitude values to the Thingspeak channel
def upload_cloud():
    lat = get_latitude(msgdata) # From GPS_API.py
    long = get_longitude(msgdata) # From GPS_API.py

    lat = round(lat, 4) #Rounds lat for readability
    long = round(long, 4) #Rounds long for readability

    params = urllib.urlencode({'field1': lat,'field2': long, 'key':key })
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept" : "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print("Lat:",lat)
        print("Long:",long)
        print(response.status, response.reason)
        data = response.read()
        conn.close()
    except KeyboardInterrupt:
        print("Connection Failed")

if __name__ == "__main__":
    start_gps_receiver(ser, msgdata)
    time.sleep(2)
    ready_gps_receiver(msgdata)
    while True:
        upload_cloud()
        time.sleep(sleep) 

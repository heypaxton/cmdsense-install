from sense_hat import SenseHat  
import time  
import sys  
import requests
import json
  
# --------- User Settings ---------
SensorName = "Pilot1"
BUCKET_NAME = ":crown: " + SensorName + " Data"
BUCKET_KEY = "sensehat"
ACCESS_KEY = "LuErsCFNDWS9rhdC3RkR4ZyatPbfR9KE"
SENSOR_LOCATION_NAME = "Base"
MINUTES_BETWEEN_SENSEHAT_READS = 0.1
# ---------------------------------

sense = SenseHat()  
  
while True:
    # Read the sensors
    temp_c = sense.get_temperature()
    humidity = sense.get_humidity() 
    pressure_mb = sense.get_pressure()
    #tempPressure = sense.get_temperature_from_pressure()
    orient = sense.orientation
    orientRaw = sense.orientation_radians
    compass = sense.compass
    compassRaw = sense.compass_raw
    gyro = sense.gyro
    gyroRaw = sense.gyro_raw
    accel = sense.accel
    accelRaw = sense.accel_raw

    # Format the data
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    temp_f = float("{0:.3f}".format(temp_f))
    humidity = float("{0:.3f}".format(humidity))
    pressure_mb = float("{0:.3f}".format(pressure_mb))
    orient['pitch'] = float("{0:.3f}".format(orient['pitch']))
    orient['roll'] = float("{0:.3f}".format(orient['roll']))
    orient['yaw'] = float("{0:.3f}".format(orient['yaw']))
    orientRaw['pitch'] = float("{0:.3f}".format(orientRaw['pitch']))
    orientRaw['roll'] = float("{0:.3f}".format(orientRaw['roll']))
    orientRaw['yaw'] = float("{0:.3f}".format(orientRaw['yaw']))
    compass = float("{0:.3f}".format(compass))
    compassRaw['x'] = float("{0:.3f}".format(compassRaw['x']))
    compassRaw['y'] = float("{0:.3f}".format(compassRaw['y']))
    compassRaw['z'] = float("{0:.3f}".format(compassRaw['z']))
    gyro['pitch'] = float("{0:.3f}".format(gyro['pitch']))
    gyro['roll'] = float("{0:.3f}".format(gyro['roll']))
    gyro['yaw'] = float("{0:.3f}".format(gyro['yaw']))
    gyroRaw['x'] = float("{0:.3f}".format(gyroRaw['x']))
    gyroRaw['y'] = float("{0:.3f}".format(gyroRaw['y']))
    gyroRaw['z'] = float("{0:.3f}".format(gyroRaw['z']))
    accel['pitch'] = float("{0:.3f}".format(accel['pitch']))
    accel['roll'] = float("{0:.3f}".format(accel['roll']))
    accel['yaw'] = float("{0:.3f}".format(accel['yaw']))
    accelRaw['x'] = float("{0:.3f}".format(accelRaw['x']))
    accelRaw['y'] = float("{0:.3f}".format(accelRaw['y']))
    accelRaw['z'] = float("{0:.3f}".format(accelRaw['z']))

    print('test: {}'.format(orientRaw))

    # Stream to cloud 
    dweet = requests.post("https://dweet.io/dweet/for/sitesense-sensor", data={
	'humidty': humidity,
    	'temp': temp_f,
    	'pressure': pressure_mb,
    	'orientPitch': orient['pitch'], 
	'orientRoll': orient['roll'], 
	'orientYaw': orient['yaw'], 
	'orientRawPitch': orientRaw['pitch'],
	'orientRawYaw': orientRaw['yaw'],
	'orientRawRoll': orientRaw['roll'],
    	'compass': compass,
    	'compassRawX': compassRaw['x'], 
	'compassRawY': compassRaw['y'], 
	'compassRawZ': compassRaw['z'],
    	'gyroPitch': gyro['pitch'], 
	'gyroRoll': gyro['roll'], 
	'gyroYaw': gyro['yaw'],
    	'gyroRawX': gyroRaw['x'], 
	'gyroRawY': gyroRaw['y'], 
	'gyroRawZ': gyroRaw['z'],
    	'accelPitch': accel['pitch'], 
	'accelRoll': accel['roll'], 
	'accelYaw': accel['yaw'],
    	'accelRawX': accelRaw['x'], 
	'accelRawY': accelRaw['y'], 
	'accelRawZ': accelRaw['z']
    })
    print(dweet)



    time.sleep(60*MINUTES_BETWEEN_SENSEHAT_READS)

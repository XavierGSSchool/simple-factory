import time
import json
from sensor_factory import SensorFactory

# load in the config.json file
def load_config(path="config.json"):
    with open(path) as f:
        return json.load(f)

# load our config and sensor from config
config = load_config()
sensor = SensorFactory.create_sensor(config)

# define out sensor for exiting
sensor_in_use = config.get("mode")

# set flag for DHT sensor
using_DHT = True if sensor_in_use == "dht11" else False

# where we get the temp reading
try:
    while True:
        temp = sensor.get_temperature()
        if temp is not None:
            temp_f = round(temp * 1.8 + 32, 2)
            print(f"Reading: {temp_f}°F")
        time.sleep(0.1)
except KeyboardInterrupt:
    if(using_DHT):
        # need to call function to clse DHT connection
        sensor.cleanup()
    print("Exiting.")
from machine import Pin, SoftI2C
import max30100, gc

# I2C Configuration using SoftI2C
sda = Pin(21)  # Define the SDA (Serial Data) pin for I2C communication
scl = Pin(22)  # Define the SCL (Serial Clock) pin for I2C communication
i2c = SoftI2C(scl=scl, sda=sda)  # Create an I2C instance using defined pins

# Heart Rate and SpO2 Sensor Configuration
sensor = max30100.MAX30100(
    i2c,                        # Use the I2C instance created earlier for communication
    mode=0x03,                  # Set the mode of the MAX30100 sensor (e.g., Heart rate and SpO2 mode)
    sample_rate=100,            # Set the sampling rate for sensor readings (e.g., 100 samples/second)
    led_current_red=11.0,       # Set the LED current for red LED (in mA)
    led_current_ir=11.0         # Set the LED current for IR LED (in mA)
)

# Main Loop
while True:
    sensor.read_sensor()  # Read sensor data from the MAX30100 (both IR and Red LED values)
    
    raw_spo2 = sensor.ir   # Store the raw SpO2 value (IR LED data)
    raw_heartrate = sensor.red  # Store the raw heart rate value (Red LED data)

    # Calculate SpO2 and Heart Rate from raw values
    spo2_value = min((raw_spo2 / 100), 100) if raw_spo2 else 0  # Normalize SpO2 value and cap at 100%
    heartrate_value = (raw_heartrate / 200) if raw_heartrate else 0  # Normalize heart rate value

    # Update global variables with rounded values as strings
    spo2 = str(round(spo2_value))      # Convert the rounded SpO2 value to string for display
    heartrate = str(round(heartrate_value))  # Convert the rounded heart rate value to string

    # Run garbage collection after each read to free up memory
    gc.collect()  # Free unused memory blocks to avoid memory overflow

    # Print SpO2 and Heart Rate values to the console
    print(f"SpO2: {spo2}%\tHeartrate: {heartrate} bpm")

    # Optional: Add a delay to control the sampling rate (e.g., time.sleep(1) for 1-second delay)
    # sleep(1)
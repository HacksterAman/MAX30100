# MAX30100 MicroPython Library for Heart Rate and SpO2 Measurement

This repository contains a MicroPython library for interfacing with the **MAX30100** Heart Rate and SpO2 sensor. The library has been optimized for minimal memory usage and efficient sensor readings using `SoftI2C`. It is compatible with various microcontrollers such as **ESP8266**, **ESP32**, and **Raspberry Pi Pico**, making it versatile and easy to integrate into multiple platforms.

## Key Features

- **Optimized Memory Usage**: Improved memory management through periodic garbage collection to free unused memory blocks, ensuring smooth operation on memory-constrained devices.
- **SoftI2C Compatibility**: Uses `SoftI2C` for I2C communication, providing flexibility in pin configuration and enabling the use of any available GPIO pins for I2C communication.
- **High Sampling Rate Support**: Capable of configuring the sensor for high sampling rates to capture detailed heart rate and SpO2 data.
- **Cross-Platform**: Works seamlessly with popular MicroPython-supported platforms like ESP8266, ESP32, and Raspberry Pi Pico.

## Installation

To use this library, copy the `max30100.py` file into your project directory or upload it directly to your MicroPython board.

## Usage Example

Below is a sample script that demonstrates how to use the library to read heart rate and SpO2 values from the MAX30100 sensor:

```python
# example.py
from machine import Pin, SoftI2C  # Import necessary classes from the machine module
import max30100, gc               # Import the max30100 library and garbage collection module

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

# Main Loop to Read and Display Sensor Data
while True:
    sensor.read_sensor()  # Read sensor data from the MAX30100 (both IR and Red LED values)
    
    raw_spo2 = sensor.ir         # Store the raw SpO2 value (IR LED data)
    raw_heartrate = sensor.red   # Store the raw heart rate value (Red LED data)

    # Calculate SpO2 and Heart Rate from raw values
    spo2_value = min((raw_spo2 / 100), 100) if raw_spo2 else 0  # Normalize SpO2 value and cap at 100%
    heartrate_value = (raw_heartrate / 200) if raw_heartrate else 0  # Normalize heart rate value

    # Convert rounded values to strings for display or further use
    spo2 = str(round(spo2_value))
    heartrate = str(round(heartrate_value))

    # Run garbage collection after each read to free up memory
    gc.collect()  # Free unused memory blocks to prevent memory overflow on constrained devices

    # Print SpO2 and Heart Rate values to the console
    print(f"SpO2: {spo2}%\tHeartrate: {heartrate} bpm")

    # Optional: Add a delay (e.g., sleep(1)) if you want to reduce the sampling rate
    # sleep(1)
```

## Library API

### `MAX30100` Class

The `MAX30100` class provides an interface for the MAX30100 sensor.

#### Initialization

```python
sensor = max30100.MAX30100(i2c, mode=0x03, sample_rate=100, led_current_red=11.0, led_current_ir=11.0)
```

- **i2c**: An instance of I2C (can be hardware or software I2C).
- **mode**: Operating mode of the sensor (e.g., Heart Rate and SpO2 mode).
- **sample_rate**: Sampling rate for sensor readings (e.g., 100 samples/second).
- **led_current_red**: LED current for the red LED in mA (e.g., 11.0 mA).
- **led_current_ir**: LED current for the IR LED in mA (e.g., 11.0 mA).

#### Methods

- **`read_sensor()`**: Reads the raw sensor values for heart rate and SpO2.
- **`ir`**: Returns the raw IR value for SpO2 measurement.
- **`red`**: Returns the raw red LED value for heart rate measurement.

## Memory Optimization

To address memory constraints on small microcontrollers, the library includes automatic garbage collection using the `gc.collect()` method after each sensor read. This helps in freeing up unused memory blocks, ensuring the program runs smoothly without memory overflow.

## Compatibility

This library has been tested on the following platforms:

- **ESP32**: Ideal for projects requiring both Wi-Fi and Bluetooth connectivity.
- **ESP8266**: Suitable for simpler IoT projects.
- **Raspberry Pi Pico**: Great for cost-effective and low-power projects.

## Contribution

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for additional features. This library is continuously improved to provide a robust solution for using the MAX30100 sensor in MicroPython projects.

## License

This library is open-source and available under the MIT License. Please feel free to use and modify it as per your project requirements.

## Acknowledgements

Special thanks to the open-source community and MicroPython developers for their valuable contributions and support.

---

This README provides a comprehensive overview of the library's capabilities, usage, and key features. Feel free to modify or expand it as needed based on any additional features or improvements you make to the library!

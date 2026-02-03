"""Arduino Case Temperature Sensor Reader.

This module reads temperature data from an Arduino-based case temperature
sensor via serial connection and saves the readings to sensor files.
"""
import logging
import os
import time
from getpass import getuser

import serial
import serial.tools.list_ports

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("ct_sensor")
logger.info("Starting CT Sensor Reader")

# Arduino communication constants
MAGIC = "CT_SENSOR"  # Magic string to identify valid sensor data
BAUD = 9600  # Serial communication baud rate
SCAN_TIMEOUT = 2  # Timeout in seconds when scanning for sensor

# Sensor data storage location
SENSOR_FILE_FOLDER = f"/home/{getuser()}/.sensors"

logger.info(f"Sensor file folder: {SENSOR_FILE_FOLDER}")

def find_sensor_port():
    """Scan serial ports to find the Arduino sensor.

    Returns:
        str: Device path of the sensor port (e.g., '/dev/ttyACM0'),
             or None if not found.
    """
    # Get all available serial ports
    ports = serial.tools.list_ports.comports()

    # Filter for ACM devices (Arduino typically shows up as ttyACMx on Linux)
    ports = [p for p in ports if "ACM" in p.device]

    # Try each potential port
    for p in ports:
        try:
            # Connect and read initial data
            ser = serial.Serial(p.device, BAUD, timeout=SCAN_TIMEOUT)
            time.sleep(1.5)  # Give the board time to start sending
            line = ser.readline().decode(errors="ignore").strip()
            ser.close()

            # Check if this port is our sensor
            if MAGIC in line:
                return p.device
        except (serial.SerialException, OSError):
            # Port unavailable or not accessible, continue searching
            pass
    return None

def read_sensor(port):
    """Read temperature data from the sensor and save to files.

    Args:
        port (str): Serial port path to read from.
    """
    with serial.Serial(port, BAUD, timeout=2) as ser:
        while True:
            try:
                # Read and parse serial data
                line = ser.readline().decode(errors="ignore").strip()
                if MAGIC in line:
                    parts = line.split(",")
                    if len(parts) == 3:
                        # Convert temperatures to millidegrees (integer format)
                        temp_front = int(float(parts[1]) * 1000)
                        temp_rear = int(float(parts[2]) * 1000)
                        temp_diff = temp_rear - temp_front
                        logger.debug(f"Front Case: {temp_front}")
                        logger.debug(f"Rear Case: {temp_rear}")
                        logger.debug(f"Temp Difference: {temp_diff}")

                        # Write temperature data to sensor files
                        with open(os.path.join(SENSOR_FILE_FOLDER, "temp_diff.sens"), "w") as f:
                            f.write(str(temp_diff))
                        with open(os.path.join(SENSOR_FILE_FOLDER, "temp_front.sens"), "w") as f:
                            f.write(str(temp_front))
                        with open(os.path.join(SENSOR_FILE_FOLDER, "temp_rear.sens"), "w") as f:
                            f.write(str(temp_rear))

                # Small delay to prevent CPU spinning
                time.sleep(0.1)
            except serial.SerialException:
                logger.error("Connection lost.")
                break

def main():
    """Main loop to continuously monitor the temperature sensor.

    Scans for the sensor, reads data when connected, and retries
    if the sensor is disconnected or not found.
    """
    while True:
        port = find_sensor_port()

        if port:
            logger.debug(f"Sensor found on {port}")
            read_sensor(port)
        else:
            logger.debug("Sensor not found. Retrying in 3s...")
            time.sleep(3)

if __name__ == "__main__":
    main()

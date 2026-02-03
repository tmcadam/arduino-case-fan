import os
import serial
import serial.tools.list_ports
import time
from getpass import getuser

MAGIC = "CT_SENSOR"
BAUD = 9600
SCAN_TIMEOUT = 2
SENSOR_FILE_FOLDER = f"/home/{getuser()}/.sensors"

def find_sensor_port():
    ports = serial.tools.list_ports.comports()

    ports = [p for p in ports if "ACM" in p.device]

    for p in ports:

        try:
            ser = serial.Serial(p.device, BAUD, timeout=SCAN_TIMEOUT)
            time.sleep(1.5)  # Give the board time to start sending
            line = ser.readline().decode(errors="ignore").strip()
            ser.close()

            if MAGIC in line:
                return p.device
        except:
            pass
    return None

def read_sensor(port):
    with serial.Serial(port, BAUD, timeout=2) as ser:
        while True:
            try:
                line = ser.readline().decode(errors="ignore").strip()
                if MAGIC in line:
                    parts = line.split(",")
                    if len(parts) == 3:
                        temp_front = int(float(parts[1]) *1000)                        
                        temp_rear = int(float(parts[2]) *1000)
                        temp_diff = temp_rear - temp_front
                        print(f"Front Case:", temp_front)
                        print(f"Rear Case:", temp_rear)
                        print(f"Temp Difference:", temp_diff)
                        
                        with open(os.path.join(SENSOR_FILE_FOLDER, "temp_diff.sens"), "w") as f:
                            f.write(str(temp_diff))
                        with open(os.path.join(SENSOR_FILE_FOLDER, "temp_front.sens"), "w") as f:
                            f.write(str(temp_front))
                        with open(os.path.join(SENSOR_FILE_FOLDER, "temp_rear.sens"), "w") as f:
                            f.write(str(temp_rear))
                time.sleep(0.1)
            except serial.SerialException:
                print("Connection lost.")
                break

def main():
    while True:
        port = find_sensor_port()

        if port:
            print(f"Sensor found on {port}")
            read_sensor(port)
        else:
            print("Sensor not found. Retrying in 3s...")
            time.sleep(3)

if __name__ == "__main__":
    main()

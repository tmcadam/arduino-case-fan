import serial
import serial.tools.list_ports
import time
import winreg

MAGIC = "MAGIC_CT_SENSOR"
BAUD = 9600
SCAN_TIMEOUT = 2
OUTPUT_FILE = "C:\\Data\\case_temperature.sensor"

KEY_PATH = r"Software\HWiNFO64\Sensors\Custom\Custom Sensors\Temp0"

def find_sensor_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:

        if "usb" not in p.description.lower() or "serial" not in p.description.lower():
            continue

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

def update_registry(value):


    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY_PATH, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "Value", 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)
        print(f"Registry updated with value: {value}")
    except Exception as e:
        print(f"Failed to update registry: {e}")

def read_sensor(port):
    with serial.Serial(port, BAUD, timeout=2) as ser:
        while True:
            try:
                line = ser.readline().decode(errors="ignore").strip()
                if MAGIC in line:
                    parts = line.split(",")
                    if len(parts) == 2:
                        temp_value = parts[1]
                        print("Temp:", temp_value)

                        with open(OUTPUT_FILE, "w") as f:
                            f.write(temp_value)

                        update_registry(temp_value)

                time.sleep(1)
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

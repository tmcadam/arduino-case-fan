# Arduino Case Fan

My motherboard doesn't support a extra case temperature sensor, and I realised that the onboard motherboard temperature is not representative of case temperature.

This is a super simple Arduino sketch that reads a DS18B20 temperature sensor and posts temperatures over USB serial. It has a small python script that runs in Windows to read the serial stream from the temperature sensor.

## Windows

### HWiNFO

HWiNFO can take a sensor reading from specific registry key. The setup is documented in this forum post https://www.hwinfo.com/forum/threads/custom-user-sensors-in-hwinfo.5817/.


### FanControl

In FanControl there two options.

  - Install the HWiNFO plugin and use the custom sensor we have already added there.
    - This is not ideal as HWiNFO needs to always be running.
  - Write to a '.sensor' file and FanControl can use it as a custom sensor input.


## Linux

### Coolercontrol 

  - Similar functionality to Fancontrol. 
  - Needs lmsensors installed. Accepts custom sensors from file.
  - Needs an extra driver for the fans on the motherboard (nct6798).

```
  sudo modprobe nct6775
  sudo sensors-detect
  echo "nct6775" | sudo tee /etc/modules-load.d/nct6775.conf
```

from [this post](https://unix.stackexchange.com/questions/790419/asus-motherboard-fan-control-under-linux)


### Linux Disable Suspend/Wake

`sudo vim /etc/udev/rules.d/99-usb-serial-nosuspend.rules`

`ATTR{idVendor}=="2341", ATTR{idProduct}=="8036", ENV{ID_MM_DEVICE_IGNORE}="1"`

```
sudo udevadm control --reload
sudo udevadm trigger
```

and....

`sudo vim /etc/systemd/system/disable-ptxh-wakeup.service`

```
[Unit]
Description=Disable PTXH USB wakeup
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c "echo PTXH > /proc/acpi/wakeup"

[Install]
WantedBy=multi-user.target
```

`sudo systemctl enable disable-ptxh-wakeup`


Test with:

`systemctl suspend`


### ToDo

  - check if this blocks PC sleeping
  - bundle Python into an exe, or rewrite in something more suitable
  - tidy up hardware
    - use a smaller Atmega32u4 board, or custom build one
    - connect internally to USB
      - buy a splitter and adapter
      - make a custom board that plugs straight in

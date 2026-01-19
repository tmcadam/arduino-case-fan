# Arduino Case Fan

My motherboard doesn't support a extra case temperature sensor, and I realised that the onboard motherboard temperature is not representative of case temperature.

This is a super simple Arduino sketch that reads a DS18B20 temperature sensor and posts temperatures over USB serial. It has a small python script that runs in Windows to read the serial stream from the temperature sensor.


### HWiNFO

HWiNFO can take a sensor reading from specific registry key. The setup is documented in this forum post https://www.hwinfo.com/forum/threads/custom-user-sensors-in-hwinfo.5817/.


### FanControl

In FanControl there two options.

  - Install the HWiNFO plugin and use the custom sensor we have already added there.
    - This is not ideal as HWiNFO needs to always be running.
  - Write to a '.sensor' file and FanControl can use it as a custom sensor input.


### ToDo

  - check if this blocks PC sleeping
  - bundle Python into an exe, or rewrite in something more suitable
  - tidy up hardware
    - use a smaller Atmega32u4 board, or custom build one
    - connect internally to USB
      - buy a splitter and adapter
      - make a custom board that plugs straight in

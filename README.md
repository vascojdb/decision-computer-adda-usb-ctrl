# Python application for Decision-Computer USB 14/16bit Acquisition Boards
This repository contains a Python library/application example to control USB 14/16bit acquisition boards from [Decision-Computer](https://www.decision-computer.de/index.html).  
You can include or modify the library according to your needs. 

The boards can be found and bought from the producer here: [https://www.decision-computer.de/Produkte/Menue-usb-e.html](https://www.decision-computer.de/Produkte/Menue-usb-e.html)  
The link contains additional **Windows drivers**, all **documentation** and additional **source code**.

If you wish to control DIO boards from the same producer, check my other repositories

## Compatible devices:
The following devices are compatible with this driver and standalone application:
  - USB 14/16bit Acquisition Board

## Requirements:
The only requirements are **Python 2.7** *(it has not been tested in Python 3, but probably it will work)* and **PySerial**.

## Running:
Just run the application with 'help' from the terminal and you will see the available commands. By default the serial port for the device is configured as **/dev/ttyttyACM0**, you may change it on the source file if you wish.
```shell
$ python DecisionUsbadda.py help
DecisionUsbadda.py - Interface with Decision-Computer 14/16bit USB data acquisition board
Usage: python DecisionUsbadda.py <see below>
  DIO: Read a channel:        dio_read <0-4>
       Write to a channel:    dio_write <0-4> <0x00-0xFF/0-255>
  ADC: Set range:             adc_range <0-3>
       Set samples per read:  adc_samples <0-255>
       Disable channel:       adc_disable_channel <0-15>
       Enable channel:        adc_enable_channel <0-15>
       Read channels:         adc_read/adc_read_all
       Read channel:          adc_read_channel <0-15>
  DAC: Set channel range:     dac_range <0-1> <0-15>
       Set channel value:     dac_set <0-1> <0x0000-0xFFFF/0-65535>
       Adjust channel value:  dac_adjust <0-1> <0x0000-0xFFFF/0-65535>
       Reset channel to GND:  dac_reset <0-1>
```

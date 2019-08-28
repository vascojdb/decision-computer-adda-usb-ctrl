#!/usr/bin/python
__author__ = "Vasco baptista"
__copyright__ = "Copyright 2019, Vasco Baptista"
__version__ = "1.0"
__maintainer__ = "Vasco Baptista"
__email__ = "vascojdb@gmail.com"

import sys
import serial

class DecisionUsbadda:
    """
    Decision-Computer USB 14/16 Bit Data Acquisition Board
    See operation manual for details
    """
    def __init__(self, port='/dev/ttyACM0', card_id=0):
        self.card_id = card_id
        try:
            print('Opening connection to Data Acquisition board on port {} at 9600bps'.format(port))
            self.ser = serial.Serial(port=port, baudrate=9600, timeout=2.0, write_timeout=2.0)
        except:
            print('Error opening serial port {}. Exiting...'.format(port))
            exit(1)

    def __exit__(self):
        if self.ser.is_open:
            self.ser.close()
    
    def __execute_serial_command(self, command, expect_bytes):
        #print('Command: {}'.format(command))
        self.ser.write(command)
        # We expect the unit to echo back the command:
        ret = self.ser.read(len(command))
        if ret != command:
            print('Unexpected echo: {}, expected {}. Exiting...'.format(str(ret), str(command)))
            exit(1)
        # If we dont expect anything, return empty array:
        if expect_bytes <= 0:
            return bytes([])
        # Read the data we are expecting:
        ret = self.ser.read(expect_bytes)
        #print('Response: {}'.format(ret))
        if len(ret) < expect_bytes:
            print('A timeout occured while waiting for an expected response. Exiting...')
            exit(1)
        return ret
    
    def dio_write(self, dio_channel, value):
        """Write output value to DIO channel"""
        assert 0 <= dio_channel <= 4
        assert 0 <= value <= 255
        command = b'S%xW%x%02x' % (self.card_id, dio_channel, value)
        self.__execute_serial_command(command, expect_bytes=0)

    def dio_read(self, dio_channel):
        """Read DIO channel back"""
        assert 0 <= dio_channel <= 4
        command = b'S%xR%x' % (self.card_id, dio_channel)
        ret = self.__execute_serial_command(command, expect_bytes=5)
        value = int(ret[3:5], 16)
        assert 0 <= value <= 255
        return value
        
    def adc_range(self, adc_range):
        """Set ADC range - See manual for values"""
        assert 0 <= adc_range <= 3
        command = b'S%xAG%u' % (self.card_id, adc_range)
        self.__execute_serial_command(command, expect_bytes=0)
        
    def adc_samples(self, samples):
        """Set ADC number of samples per read"""
        assert 0 <= samples <= 255
        command = b'S%xAA%02x' % (self.card_id, samples)
        self.__execute_serial_command(command, expect_bytes=0)

    def adc_disable_channel(self, adc_channel):
        """Disable an ADC channel"""
        assert 0 <= adc_channel <= 15
        command = b'S%xAD%x' % (self.card_id, adc_channel)
        self.__execute_serial_command(command, expect_bytes=0)
        
    def adc_enable_channel(self, adc_channel):
        """Disable an ADC channel"""
        assert 0 <= adc_channel <= 15
        command = b'S%xAE%x' % (self.card_id, adc_channel)
        self.__execute_serial_command(command, expect_bytes=0)
        
    def adc_read_all(self):
        """Reads all the ADC channels"""
        command = b'S%xAR' % (self.card_id)
        ret = self.__execute_serial_command(command, expect_bytes=96)
        list_values = ret[1:].split('P')
        adc_list = []
        for pair in list_values:
            channel = int(pair[0], 16)
            value = int(pair[1:], 16)
            adc_list.append(value)
            #print('[%x]=0x%02x=%i' % (channel, value, value))
        return adc_list
        
    def adc_read_channel(self, adc_channel):
        """Reads one specific ADC channel"""
        assert 0 <= adc_channel <= 15
        command = b'S%xAR' % (self.card_id)
        ret = self.__execute_serial_command(command, expect_bytes=96)
        list_values = ret[1:].split('P')
        for pair in list_values:
            channel = int(pair[0], 16)
            if adc_channel == channel:
                value = int(pair[1:], 16)
                #print('[%x]=0x%02x=%i' % (channel, value, value))
                return value;
    
    def dac_set(self, dac_channel, value):
        """Set DAC channel output to a value"""
        assert 0 <= dac_channel <= 1
        assert 0 <= value <= 65535
        command = b'S%xD%u%04x' % (self.card_id, dac_channel, value)
        self.__execute_serial_command(command, expect_bytes=0)
        
    def dac_adjust(self, dac_channel, value):
        """Adjusts DAC channel output to a value"""
        assert 0 <= dac_channel <= 1
        assert 0 <= value <= 65535
        command = b'S%xDJ%u%04x' % (self.card_id, dac_channel, value)
        self.__execute_serial_command(command, expect_bytes=0)

    def dac_range(self, dac_channel, range):
        """Set DAC output range"""
        assert 0 <= dac_channel <= 1
        assert 0 <= range <= 15
        command = b'S%xDG%u%x' % (self.card_id, dac_channel, range)
        self.__execute_serial_command(command, expect_bytes=0)

    def dac_reset(self, dac_channel):
        """Resets a DAC channel to GND"""
        assert 0 <= dac_channel <= 1
        command = b'S%xDR%u' % (self.card_id, dac_channel)
        self.__execute_serial_command(command, expect_bytes=0)


def print_usage():
    """ Prints usage """
    print('{} - Interface with Decision-Computer 14/16bit USB data acquisition board'.format(sys.argv[0]))
    print('Usage: python {} <see below>'.format(sys.argv[0]))
    print('  DIO: Read a channel:        dio_read <0-4>')
    print('       Write to a channel:    dio_write <0-4> <0x00-0xFF/0-255>')
    print('  ADC: Set range:             adc_range <0-3>')
    print('       Set samples per read:  adc_samples <0-255>')
    print('       Disable channel:       adc_disable_channel <0-15>')
    print('       Enable channel:        adc_enable_channel <0-15>')
    print('       Read channels:         adc_read/adc_read_all')
    print('       Read channel:          adc_read_channel <0-15>')
    print('  DAC: Set channel range:     dac_range <0-1> <0-15>')
    print('       Set channel value:     dac_set <0-1> <0x0000-0xFFFF/0-65535>')
    print('       Adjust channel value:  dac_adjust <0-1> <0x0000-0xFFFF/0-65535>')
    print('       Reset channel to GND:  dac_reset <0-1>')


if __name__ == "__main__":
    if len(sys.argv) < 1 or len(sys.argv) > 4:
        print_usage()
        exit(1)

    # Gets the action and the valie1 number to be used, as well as the value2 if required:
    action = sys.argv[1]
    value1 = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0
    value2 = int(sys.argv[3], 0) if len(sys.argv) > 3 else 0

    if action == 'help':
        print_usage()
        exit(0)

    # Creates the object:
    adda = DecisionUsbadda(port='/dev/ttyACM0', card_id=0)
    
    # Perform action:
    if action == 'dio_read':
        value = adda.dio_read(value1)
        print(value)
    elif action == 'dio_write':
        adda.dio_write(value1, value2)
    elif action == 'adc_range':
        adda.adc_range(value1)
    elif action == 'adc_samples':
        adda.adc_samples(value1)
    elif action == 'adc_disable_channel':
        adda.adc_disable_channel(value1)
    elif action == 'adc_enable_channel':
        adda.adc_enable_channel(value1)
    elif action == 'adc_read_all' or action == 'adc_read':
        value = adda.adc_read_all()
        print(value)
    elif action == 'adc_read_channel':
        value = adda.adc_read_channel(value1)
        print(value)
    elif action == 'dac_range':
        adda.dac_range(value1, value2)
    elif action == 'dac_set':
        adda.dac_set(value1, value2)
    elif action == 'dac_adjust':
        adda.dac_adjust(value1, value2)
    elif action == 'dac_reset':
        adda.dac_reset(value1)
    else:
        print_usage()
        exit(1)

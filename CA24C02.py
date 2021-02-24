  
import smbus2
import time  
import sys
import random



class CA24C02(object):
    def __init__(self):
        self.i2c_bus = 0  # EEPROM is located in i2c-0 bus
        self._dev_address = 0x50     # CA24C02 i2c-0 address is 0x50
    
    def random_byte_read(self, data_address):

        time.sleep(0.01)
        write_msg = smbus2.i2c_msg.write(self._dev_address,[data_address])
        read_msg = smbus2.i2c_msg.read(self._dev_address, length=1 )

        with smbus2.SMBus(self.i2c_bus) as bus:
            bus.i2c_rdwr(write_msg, read_msg)

        # byorder doesn't seem to do anything
        data_byte = list(read_msg)[0]
        
        print('Reading addr[0x{:02X}] = 0x{:02X}'.format(data_address, data_byte))

        return data_byte


    def random_byte_write(self, data_address, data_byte):
        
        print('Writing addr[0x{:02X}] = 0x{:02X}'.format(data_address, data_byte))

        smbus2.SMBus(self.i2c_bus).write_i2c_block_data(self._dev_address, data_address, [data_byte])

        time.sleep(0.01)


def main():

    help_txt = []
    help_txt.append("This program tests CA24C02 EEPROM in I2C-0 bus")
    help_txt.append("It generates random bytes and writes to all EEPROM memory addresses.")
    help_txt.append("Then it reads all memory addresses and compares retrieved value with originally stored one.")
    help_txt.append("")
    help_txt.append("Press Enter to continue...")

    input("\n".join(help_txt))

    eeprom = CA24C02()

    log = set()
    errors = []

    print("\nWriting memory in range 0x00 - 0xFF. In sequence...\n")
    for mem_address in range(256):


        # Generate random data
        random_data = random.randint(0, 255)

        # Store tuple(memory address, random data)
        log.add((mem_address, random_data))

        # Write random data
        eeprom.random_byte_write(mem_address, random_data)


    print("\nReading memory in range 0x00 - 0xFF. All addresses will be read randomly...\n")
    while len(log) > 0:

        mem_address, random_data = log.pop()
        # Read data
        retrieved_data = eeprom.random_byte_read(mem_address)
        # Check if read data equals originally stored data
        if random_data != retrieved_data:
            errors.append("Error in address 0x{:02X}. Written 0x{:02X}, read 0x{:02X}".format(mem_address,random_data,retrieved_data))

    if len(errors) == 0:
        print("\nTest finished. EEPROM works fine !\n")
    else:
        for error in errors:
            print(error)


if __name__ == '__main__':  
    try:  
        main()  
    except KeyboardInterrupt:  
        sys.exit(0)
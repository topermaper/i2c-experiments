  
import smbus  
import time  
import sys  
bus = smbus.SMBus(0)  
address = 0x60          # Audio driver address

#https://www.ti.com/lit/ds/slos488f/slos488f.pdf?ts=1613344836211

def main():
    '''
    print("Argument List:{}".format(str(sys.argv)))
    if len(sys.argv) != 2:        sys.exit(0) 

    toint = int(sys.argv[1],16)
    data = toint.to_bytes()

    print(type(data))
    print(data)
    '''
    reg_address = 0
    bus.write_byte_data(address,2,11)  
    while reg_address < 16:
        print('checking register',reg_address)
        # send data  
        #bus.write_byte(address,data)  
          
        # request data
        print ("TPA61302: {0:08b}".format(bus.read_byte_data(address,reg_address)))
          
        time.sleep(0.01)
        reg_address += 1

if __name__ == '__main__':  
    try:  
        main()  
    except KeyboardInterrupt:  
        gpio.cleanup()  
        sys.exit(0)  
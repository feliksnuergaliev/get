import smbus 
import time
class MCP3021:
    def __init__(self, dynamic_range,verbose = False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        if self.verbose:
            print(f"Принятые данные: {data}, Старший байт: {upper_data_byte:x}, Младший байт: {lower_data_byte:x}, Число: {number}")
        return number

    def get_voltage(self):
        word = self.bus.read_word_data(self.address, 0)
        b0 = word & 0x0F
        b1 = (word >> 8) & 0x0F

        code = ((b0 & 0x0F) << 6) | (b1 >> 2)

        return code * self.dynamic_range / 1024

if __name__ == "__main__":

    try:
        adc=MCP3021(5.0, True)
        while True:
            voltage = adc.get_voltage()
            print(f"U = {voltage:.3f} B")
        
    finally:
        adc.deinit()
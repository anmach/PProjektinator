from openbci import wifi as bci

class ControllerBCI():
    """ Kontroler do czytania myśli """

    def __init__(self):        
        self.__instructions = []

        shield = bci.OpenBCIWiFi(ip_address=ip_address, log=True, high_speed=True, sample_rate=sample_rate, latency=100)

    def start_reading(self):        
        shield.start_streaming(self.printData)            
        shield.loop()

    def stop_reading(self):
        shield.stop()

    def process_data():
        if(len( sample.channel_data ) != 16):
            return

        temp = str(sample.channel_data)
        inData = temp[1:len(temp)-1]

        # przetworzenie myśli

        #self.__instructions.append()

    def get_instructions(self):
        inst = self.__instructions.pop(0)
        return inst
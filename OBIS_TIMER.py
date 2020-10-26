"""

This program utilizes pyVisa which can be installed or upgraded by using
the pip command in the command window: pip install pyVisa.

VISA is standard for interacting with instruments from a computer. VISA uses
SCPI commands which is even more common. You could find a way to talk to SCPI
directly but VISA was easy due to the LabVIEW examples.

For more examples on how to use VISA and OBIS you can reference the LabVIEW
examples for our model of the OBIS Coherent Laser diode

For examples on how to use pyVISA look up the current modules doumentation
online

created by: bp 6-8-16
@author: Brae
"""


import visa
from threading import Timer # This is our timer module
class OBIS():
    def __init__(self, com= "COM6"):
        """ For the PA800B the OBIS is a serial communication at 'COM5'
        this may differ between computers. You can look it up by searching
        for VISA Interactive Control and replacing the COM5 above with whatever
        COM channel the OBIS coherent is located.

        You can also find it by opening the OBIS Coherent connect software and
        trying to access each of the 'ASRL' resources listed from:

        rm.list_resources()

        If pyVISA is unable to connect to the resource there is a chance that is
        the correct resource.

        pyVISA essentially  uses SCPI (skippy!) commands (e.g "syst1:diod:hour?")
        to interface with the instrument. SCPI is pretty common and if there is
        something you want to learn from the laser you can try googling what information
        or command your interested in plus SCPI command:

        model version SCPI command

        diode hours SCPI command

        

        """
        self.rm = visa.ResourceManager()

        self.obis = self.rm.open_resource(com)
        self.turnoff=False
    def get_diod_hour(self):
        hour=self.obis.query("syst1:diod:hour?",0.1).split('\r')
        self.obis.read()
        return hour[0]
    def get_model(self):
        model=self.obis.query("*IDN?").split('\r')
        self.obis.read()
        return model[0]
        
    def get_mode(self):
        """Only returns two of the possible modes"""
        modes={"CWP":'Constant Power', "CWC":'Constant Current'}
        mode=self.obis.query("sour1:am:sour?",0.1).split('\r')
        self.obis.read()
        return modes[mode[0]]
    def get_status(self):
        status=self.obis.query("sour1:am:stat?",0.1).split('\r')
        self.obis.read()
        return status[0]
    def get_max_power_level(self):
        power=self.obis.query("sour1:pow:nom?",0.1).split('\r')
        self.obis.read()
        return power[0]
    def get_power_level(self):
        power=self.obis.query("sour1:pow:lev:imm:ampl?",0.1).split('\r')
        self.obis.read()
        return power[0]
    def get_wavelength(self):
        wavelength=self.obis.query("syst1:inf:wav?",0.1).split('\r')
        self.obis.read()
        
        return wavelength[0]
    def change_status(self, on=False):
        if on:
            command="ON"
        else:
            command = "OFF"
        self.obis.write("sour1:am:stat {}".format(command))
        self.obis.read()
       
        
    def set_power_level(self,level):
        """mW input and is converted to watts"""
        level=level/1000 # convert to watts
        max1=self.get_max_power_level()
        #self.obis.read()
        if eval(max1) < level:
            return ("ERROR: Too Power Level Too High!!")
        else:
            power=self.obis.write("sour1:pow:lev:imm:ampl {}".format(level))
            self.obis.read()
            return ("Change Succesful")
    def set_timer(self, minutes=60):
        seconds=minutes*60
        self.t=Timer(seconds, self.change_status)
        self.t.start()
    def gui_set_timer(self,minutes=60):
        seconds=minutes*60
        self.t=Timer(seconds,self.changeflag)
        self.t.start()
    def changeflag(self):
        self.turnoff=True
    def close(self):
        self.obis.close()
    
        
        
        
        
        
    
        
        
        
        

    


from rflib import *


def configure_yardstick(d, frequency, modulation, baudrate, deviation, amp):
    d.setFreq(frequency)
    if modulation == 'AM270' or modulation == 'AM650':
        if 'AM270' in modulation:
            configure_am270(d)
        else:
            configure_am650(d)
    else:
        if 'FM238' in modulation:
            configure_fm238(d)
        else:
            configure_fm476(d)
    d.setChannel(0)
    d.setMdmSyncMode(0)
    if baudrate != 0:
        d.setMdmDRate(baudrate)
    if amp != False:
        d.setAmpMode(1)
    else:
        d.setAmpMode(0)
    if deviation != 0:
        d.setMdmDeviatn(deviation)

def configure_am270(d):
    d.setMdmDRate(3793)  # Set your desired data rate
    d.setMdmModulation(MOD_ASK_OOK)  # Set modulation to ASK/OOK
    d.setMdmChanSpc(25000)  # Set channel spacing to 25 kHz
    d.calculatePktChanBW()

def configure_am650(d):
    d.setMdmDRate(3793)
    d.setMdmModulation(MOD_ASK_OOK)
    d.setMdmChanSpc(25000)
    d.setMdmChanBW(65000)

def configure_fm238(d):
    d.setMdmDRate(4797)
    d.setMdmModulation(MOD_2FSK)  # Set modulation to 2FSK
    d.setMdmChanSpc(25000)
    d.calculatePktChanBW()
    d.setMdmDeviatn(2380)

    
def configure_fm476(d):
    d.setMdmDRate(4797)
    d.setMdmModulation(MOD_2FSK)
    d.setMdmChanSpc(25000)
    d.calculatePktChanBW()
    d.setMdmDeviatn(4760)

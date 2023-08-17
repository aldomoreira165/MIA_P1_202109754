import ctypes
import struct
import random
import datetime
from utilities import coding_str

const = 'I q I 1s'

class Mbr(ctypes.Structure):
    _fields_ = [
        ('tamano', ctypes.c_int),
        ('time', ctypes.c_long),
        ('dsk_signature', ctypes.c_int ),
        ('fit', ctypes.c_char)
    ]

    def __init__(self):
        self.tamano = 0
        self.time = 0
        self.dsk_signature = 0
        self.fit = b'\0'


    def set_tamano(self, tamano):
        self.tamano = tamano

    def set_time(self):
        self.time= int(datetime.datetime.now().timestamp())

    def set_fit(self, fit):
        self.fit = coding_str(fit, 1)

    def set_dsk_signature(self):
        self.dsk_signature = random.randint(1, 1000)

    def set_infomation(self, tamano, fit):
        self.set_tamano(tamano)
        self.set_fit(fit)
        self.set_dsk_signature()
        self.set_time()

    
    def display_info(self):
        print(f"tamano: {self.tamano}")
        print(f"fit: {self.fit}")
        print(f"dsk_signature: {self.dsk_signature}")
        print(f"fecha: {self.time}")
        

    def doSerialize(self):
        return struct.pack(
            const,
            self.tamano,
            self.time,
            self.dsk_signature,
            self.fit
        )

    def doDeserialize(self, data):
        self.tamano, self.time, self.dsk_signature, self.fit = struct.unpack(const, data)
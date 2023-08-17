import ctypes
import struct
import random
import datetime
from utilities import coding_str

const = ''

class Particion(ctypes.Structure):
    _fields_ = [
        ('status', ctypes.c_char),
        ('type', ctypes.c_char)
        ('fit', ctypes.c_char)
        ('start', ctypes.c_int)
        ('s', ctypes.c_int)
        ('name', ctypes.c_int)
    ]

    def __init__(self):
        self.status = b'\0'
        self.type = b'\0'
        self.fit = b'\0'
        self.start = 0
        self.s = 0
        self.name = 0


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
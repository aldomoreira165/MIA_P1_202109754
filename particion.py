import ctypes
import struct
from utilities import coding_str

const = '1s 1s 1s I I 16s'

class Particion(ctypes.Structure):
    _fields_ = [
        ('status', ctypes.c_char),
        ('type', ctypes.c_char),
        ('fit', ctypes.c_char),
        ('start', ctypes.c_int),
        ('s', ctypes.c_int),
        ('name', ctypes.c_char * 16)
    ]

    def __init__(self):
        self.status = b'\0'
        self.type = b'\0'
        self.fit = b'\0'
        self.start = 0
        self.s = 0
        self.name = b'\0' * 16


    def set_status(self, status):
        self.status = coding_str(status, 1)

    def set_type(self, type):
        self.type = coding_str(type, 1)

    def set_fit(self, fit):
        self.status = coding_str(fit, 1)
    
    def set_start(self, start):
        self.start = start

    def set_s(self, s):
        self.s = s

    def set_name(self, name):
        self.name = coding_str(name, 16)

    def set_infomation(self, status, type, fit, start, s, name):
        self.set_status = status
        self.set_type = type
        self.fit = fit
        self.start = start
        self.s = s
        self.name = name

    def get_const(self):
        return const
    
    def display_info(self):
        print(f"status: {self.status}")
        print(f"type: {self.type}")
        print(f"fit: {self.fit}")
        print(f"start: {self.start}")
        print(f"s: {self.s}")
        print(f"name: {self.name}")
        

    def doSerialize(self):
        return struct.pack(
            const,
            self.status,
            self.type,
            self.fit,
            self.start,
            self.s,
            self.name
        )

    def doDeserialize(self, data):
        self.status, self.type, self.fit, self.start, self.s, self.name = struct.unpack(const, data)
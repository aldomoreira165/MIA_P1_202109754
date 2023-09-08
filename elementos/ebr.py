import ctypes
import struct
from funciones.utilities import coding_str

const = '1s 1s I I I 16s'

class Ebr(ctypes.Structure):
    _fields_ = [
        ('status', ctypes.c_char),
        ('fit', ctypes.c_char),
        ('start', ctypes.c_int),
        ('s', ctypes.c_int),
        ('next', ctypes.c_int),
        ('name', ctypes.c_char * 16)
    ]

    def __init__(self):
        self.status = b'\0'
        self.fit = b'\0'
        self.start = 0
        self.s = 0
        self.next = 0
        self.name = b'\0' * 16

    def get_const(self):
        return const
 
    def set_status(self, status):
        self.status = coding_str(status, 1)

    def set_fit(self, fit):
        self.fit = coding_str(fit, 1)

    def set_start(self, start):
        self.start = start

    def set_s(self, s):
        self.s = s

    def set_next(self, next):
        self.next = next

    def set_name(self, name):
        self.name = coding_str(name, 16)

    def set_infomation(self, status, fit, start, s, next, name):
        self.set_status(status)
        self.set_fit(fit)
        self.set_start(start)
        self.set_s(s)
        self.set_next(next)
        self.set_name(name)
    
    def display_info(self):
        print(f"status: {self.status}")
        print(f"fit: {self.fit}")
        print(f"start: {self.start}")
        print(f"s: {self.s}")
        print(f"next: {self.next}")
        print(f"name: {self.name}")
        

    def doSerialize(self):
        return struct.pack(
            const,
            self.status,
            self.fit,
            self.start,
            self.s,
            self.next,
            self.name
        )

    def doDeserialize(self, data):
        self.status, self.fit, self.start, self.s, self.next, self.name = struct.unpack(const, data)



        

        
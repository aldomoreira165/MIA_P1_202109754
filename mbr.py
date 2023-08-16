import ctypes
import struct

const = 'I'

class Mbr(ctypes.Structure):
    _fields_ = [
        ('tamano', ctypes.c_int),
    ]

    def __init__(self):
        self.tamano = 0


    def set_tamano(self, tamano):
        self.tamano = tamano

    def set_infomation(self, tamano):
        self.set_tamano(tamano)

    
    def display_info(self):
        print(f"tamano: {self.tamano}")

    def doSerialize(self):
        return struct.pack(
            const,
            self.tamano
        )

    def doDeserialize(self, data):
        self.tamano = struct.unpack(const, data)
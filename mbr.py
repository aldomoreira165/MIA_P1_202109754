import ctypes
import struct
import random
import datetime
from utilities import coding_str
from particion import Particion

const = 'I I 1s'

class Mbr(ctypes.Structure):
    _fields_ = [
        ('tamano', ctypes.c_int),
        #('time', ctypes.c_long),
        ('dsk_signature', ctypes.c_int ),
        ('fit', ctypes.c_char)
    ]

    def __init__(self):
        self.tamano = 0
        #self.time = 0
        self.dsk_signature = 0
        self.fit = b'\0'
        self.particion1 = Particion()
        self.particion2 = Particion()
        self.particion3 = Particion()
        self.particion4 = Particion()
 

    def set_tamano(self, tamano):
        self.tamano = tamano

    """def set_time(self):
        self.time= int(datetime.datetime.now().timestamp())"""

    def set_fit(self, fit):
        self.fit = coding_str(fit, 1)

    def set_dsk_signature(self):
        self.dsk_signature = random.randint(1, 1000)

    def set_infomation(self, tamano, fit):
        self.set_tamano(tamano)
        self.set_fit(fit)
        self.set_dsk_signature()
        #self.set_time()

    
    def display_info(self):
        print(f"tamano: {self.tamano}")
        print(f"fit: {self.fit}")
        print(f"dsk_signature: {self.dsk_signature}")
        #print(f"fecha: {self.time}")
        """print(f"particion 1: {self.particion1}")
        print(f"particion 2: {self.particion2}")
        print(f"particion 3: {self.particion3}")
        print(f"particion 4: {self.particion4}")"""
        

    def doSerialize(self):
        mbr_data = struct.pack(const, self.tamano, self.dsk_signature, self.fit)
        particiones_data = self.particion1.doSerialize()+ self.particion2.doSerialize() + self.particion3.doSerialize() + self.particion4.doSerialize() 
        return mbr_data + particiones_data

    def doDeserialize(self, data):
        size_mbr = struct.calcsize(const)
        size_particion1 = struct.calcsize(self.particion1.get_const())
        size_particion2 = struct.calcsize(self.particion2.get_const())
        size_particion3 = struct.calcsize(self.particion3.get_const())

        data_mrb = data[:size_mbr]
        self.tamano, self.dsk_signature, self.fit = struct.unpack(const, data_mrb)

        data_patition1 = data[size_mbr:size_mbr + size_particion1]
        self.particion1.doDeserialize(data_patition1)

        data_particion2 = data[size_mbr + size_particion1:size_mbr + size_particion1 + size_particion2]
        self.particion2.doDeserialize(data_particion2)

        data_particion3 = data[size_mbr + size_particion1 + size_particion2:size_mbr + size_particion1 + size_particion2 + size_particion3]
        self.particion3.doDeserialize(data_particion3)

        data_particion4 = data[size_mbr + size_particion1 + size_particion2 + size_particion3:]
        self.particion4.doDeserialize(data_particion4 )



        

        
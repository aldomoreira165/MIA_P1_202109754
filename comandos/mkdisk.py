import datetime
from elementos.superbloque import *
from elementos.inodo import *
from elementos.bloque_archivos import *
from elementos.mbr import Mbr
from elementos.disco import *
from funciones.utilities import coding_str

def execute_mkdisk(args):
    if args.size > 0:
        try:
            #creando disco
            discoCreado = crearDisco(args.path)

            #creando espacio de disco
            establecerEspacioDisco(discoCreado, args.size, args.unit)

            #creando mbr de disco
            mbr = Mbr()
            bytes = obtener_total_bytes(args.size, args.unit)
            date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            mbr.set_infomation(bytes, date, args.fit)

            #generando objeto mbr en el disco
            generarDatosDisco(discoCreado, 0, mbr)
            
            discoCreado.close()

            #leer 
            mbrDEs = Mbr()
            obtenerDatosDisco(args.path, 0, mbrDEs)
            mbrDEs.display_info()
            
        except Exception as e:
            print(f"Error configurando disco: {e}")
    else:
        print("Error: El tamaño del disco debe ser positivo y mayor que 0.")


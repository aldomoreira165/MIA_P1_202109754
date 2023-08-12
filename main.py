import argparse
from disco import crearDisco, establecerEspacioDisco, eliminarDisco

#para case insensitive
class CaseInsensitiveArgumentParser(argparse.ArgumentParser):
    def _get_option_tuples(self, option_string):
        return super()._get_option_tuples(option_string.lower())

def execute_mkdisk(args):
    if args.size > 0:
        discoCreado = crearDisco(args.path)
        #establecerEspacioDisco(discoCreado, args.size, args.unit)
        discoCreado.close()
    else:
        print("Error: El tamaño del disco debe ser positivo y mayor que 0.")
        
def execute_rmdisk(args):   
    confirmacion = (input("Esta seguro que desea eliminar el disco? (S/N): ")).lower()
    if confirmacion == "s":
        eliminarDisco(args.path)
    else:
        print("Eliminacion de disco cancelada")
    

def main():
    parser = CaseInsensitiveArgumentParser(description="Analizador de comandos")


    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    #mkdisk
    mkdisk_parser = subparsers.add_parser("mkdisk", help="Crear disco")   
    mkdisk_parser.add_argument("-size", required=True, type=int, help="Tamaño del disco")
    mkdisk_parser.add_argument("-path", required=True, help="Ruta donde se creará el disco")
    mkdisk_parser.add_argument("-fit", required=False, choices=["BF", "FF", "WF"], default="FF",help="Tipo de ajuste de disco (opcional)")
    mkdisk_parser.add_argument("-unit", required=False, choices=["K", "M"], default="M", help="Unidad de tamaño (opcional)")

    #rmdisk
    rmdisk_parser = subparsers.add_parser("rmdisk", help="Eliminar disco duro")
    rmdisk_parser.add_argument("-path", required=True, help="Ruta donde se encuentra el disco a eliminar")

    args = parser.parse_args()

    if args.command == "mkdisk":
        execute_mkdisk(args)
    elif args.command == "rmdisk":
        execute_rmdisk(args)
    else:
        print("Comando desconocido")



if __name__ == "__main__":
    main()
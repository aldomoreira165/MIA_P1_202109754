import os
import argparse
from mbr import Mbr
from comando import *
from disco import *


#para case insensitive
class CaseInsensitiveArgumentParser(argparse.ArgumentParser):
    def _get_option_tuples(self, option_string):
        return super()._get_option_tuples(option_string.lower())
    
def main():
    parser = CaseInsensitiveArgumentParser(description="Analizador de comandos")

    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # Nuevo comando "execute"
    execute_parser = subparsers.add_parser("execute", help="Ejecutar comando execute")
    execute_parser.add_argument("-path", required=True, help="Ruta del archivo a abrir")

    # mkdisk
    mkdisk_parser = subparsers.add_parser("mkdisk", help="Crear disco")
    mkdisk_parser.add_argument("-size", required=True, type=int, help="Tamaño del disco")
    mkdisk_parser.add_argument("-path", required=True, help="Ruta donde se creará el disco")
    mkdisk_parser.add_argument("-fit", required=False, choices=["BF", "FF", "WF"], default="FF",help="Tipo de ajuste de disco (opcional)")
    mkdisk_parser.add_argument("-unit", required=False, choices=["K", "M"], default="M", help="Unidad de tamaño (opcional)")

    # rmdisk
    rmdisk_parser = subparsers.add_parser("rmdisk", help="Eliminar disco duro")
    rmdisk_parser.add_argument("-path", required=True, help="Ruta donde se encuentra el disco a eliminar")

    #fdisk
    fdisk_parser = subparsers.add_parser("fdisk", help={"Administrar particiones de disco duro"})
    fdisk_parser.add_argument("-size", required=True, type=int, help="Tamaño de la particion")
    fdisk_parser.add_argument("-path", required=True, help="Ruta del disco en donde se creara la particion")
    fdisk_parser.add_argument("-name", required=True, help="Nombre de la particion")
    fdisk_parser.add_argument("-unit", required=False, choices=["B","K", "M"], default="K", help="Unidad de tamaño (opcional)")
    fdisk_parser.add_argument("-fit", required=False, choices=["BF", "FF", "WF"], default="WF",help="Tipo de ajuste de disco (opcional)")



    args = parser.parse_args()

    if args.command == "execute":
        if os.path.exists(args.path):
            with open(args.path, 'r') as file:
                for line in file:
                    if "mkdisk" in line:
                        # Crear un nuevo objeto args para mkdisk
                        mkdisk_args = mkdisk_parser.parse_args(line.split()[1:])
                        execute_mkdisk(mkdisk_args)
                    elif "rmdisk" in line:
                        # Crear un nuevo objeto args para rmdisk
                        rmdisk_args = rmdisk_parser.parse_args(line.split()[1:])
                        execute_rmdisk(rmdisk_args)
                    elif "fdisk" in line:
                        # Crear un nuevo objeto args para rmdisk
                        fdisk_args = fdisk_parser.parse_args(line.split()[1:])
                        execute_fdisk(fdisk_args)
        else:
            print(f"El archivo {args.path} no existe.")
    else:
        print("Comando desconocido")


if __name__ == "__main__":
    main()
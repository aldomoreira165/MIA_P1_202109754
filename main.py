import os
import argparse
from mbr import Mbr
from disco import crearDisco, establecerEspacioDisco, eliminarDisco, escribirDisco, leerDisco


#para case insensitive
class CaseInsensitiveArgumentParser(argparse.ArgumentParser):
    def _get_option_tuples(self, option_string):
        return super()._get_option_tuples(option_string.lower())

def execute_mkdisk(args):
    if args.size > 0:

        try:
            #creando disco
            discoCreado = crearDisco(args.path)

            #creando espacio de disco
            establecerEspacioDisco(discoCreado, args.size, args.unit)

            #creando mbr de disco
            mbr = Mbr()
            mbr.set_infomation(args.size, args.fit)

            #generando objeto mbr en el disco
            escribirDisco(discoCreado, 0, mbr)
            
            discoCreado.close()

            #leer 
            mbrDEs = Mbr()
            leerDisco(args.path, 0, mbrDEs)
            mbrDEs.display_info()

            """
            print("====particiones======")
            print("----particion 1 -----")
            mbrDEs.particion1.set_status("A")
            mbrDEs.particion1.display_info()
            print("----particion 2 -----")
            mbrDEs.particion2.display_info()
            print("----particion 3 -----")
            mbrDEs.particion3.display_info()
            print("----particion 4 -----")
            mbrDEs.particion4.display_info()"""
            
        except Exception as e:
            print(f"Error configurando disco: {e}")
    else:
        print("Error: El tamaño del disco debe ser positivo y mayor que 0.")
        
def execute_rmdisk(args):   
    confirmacion = (input("Esta seguro que desea eliminar el disco? (S/N): ")).lower()
    if confirmacion == "s":
        eliminarDisco(args.path)
    else:
        print("Eliminacion de disco cancelada") 


def execute_fdisk(args):
    if args.size > 0:
        if os.path.exists(args.path):
            mbrDisco = Mbr()
            leerDisco(args.path, 0, mbrDisco)

            print("antes")
            mbrDisco.particion1.display_info()

            if mbrDisco.particion1.status == b'\0':
                mbrDisco.particion1.set_status('1')
                mbrDisco.particion1.set_name(args.name)
                mbrDisco.particion1.set_fit(args.fit)

                if args.unit == "B":
                    mbrDisco.particion1.set_s(args.size)
                elif args.unit == "K":
                    size = args.size * 1024
                    mbrDisco.particion1.set_s(size)
                elif args.unit == "M":
                    size = args.size * 1024 * 1024
                    mbrDisco.particion1.set_s(size)
                else:
                    print("unidad de particion incorrecta")

            elif mbrDisco.particion2.status == b'\0':
                mbrDisco.particion2.set_status('1')
                mbrDisco.particion2.set_name(args.name)
                mbrDisco.particion2.set_fit(args.fit)

                if args.unit == "B":
                    mbrDisco.particion2.set_s(args.size)
                elif args.unit == "K":
                    size = args.size * 1024
                    mbrDisco.particion2.set_s(size)
                elif args.unit == "M":
                    size = args.size * 1024 * 1024
                    mbrDisco.particion2.set_s(size)
                else:
                    print("unidad de particion incorrecta")
            elif mbrDisco.particion3.status == b'\0':
                mbrDisco.particion3.set_status('1')
                mbrDisco.particion3.set_name(args.name)
                mbrDisco.particion3.set_fit(args.fit)

                if args.unit == "B":
                    mbrDisco.particion3.set_s(args.size)
                elif args.unit == "K":
                    size = args.size * 1024
                    mbrDisco.particion3.set_s(size)
                elif args.unit == "M":
                    size = args.size * 1024 * 1024
                    mbrDisco.particion3.set_s(size)
                else:
                    print("unidad de particion incorrecta")
            elif mbrDisco.particion4.status == b'\0':
                mbrDisco.particion4.set_status('1')
                mbrDisco.particion4.set_name(args.name)
                mbrDisco.particion4.set_fit(args.fit)

                if args.unit == "B":
                    mbrDisco.particion4.set_s(args.size)
                elif args.unit == "K":
                    size = args.size * 1024
                    mbrDisco.particion4.set_s(size)
                elif args.unit == "M":
                    size = args.size * 1024 * 1024
                    mbrDisco.particion4.set_s(size)
                else:
                    print("unidad de particion incorrecta")

            else:
                print("Ya no existen particiones libres")

            print("despues")
            mbrDisco.particion1.display_info()
            
        else:
            print("Error: El disco no existe.")
    else:
        print("Error: El tamaño de la particion debe ser positivo y mayor que 0.")

    
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
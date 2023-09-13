from comandos.mount import particiones_montadas
from elementos.disco import obtenerDatosDisco
from elementos.superbloque import Superblock

userSesion = None

def execute_login(args):

    if userSesion != None:
        print("Ya existe una sesion iniciada")
    else:
        mPartition = None
        for partition in particiones_montadas:
            if partition[0] == args.id:
                mPartition = partition
                break

        if mPartition == None:
            print("No se encontro la particion")
        else:
            TempSuperblock = Superblock()
            obtenerDatosDisco(mPartition[2], mPartition[1].start, TempSuperblock)
            TempSuperblock.get_infomation()


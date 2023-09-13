import struct
import math
import datetime
from elementos.superbloque import *
from elementos.inodo import *
from elementos.fileblock import *
from elementos.folderblock import *
from elementos.disco import *
from funciones.utilities import coding_str
from comandos.mount import particiones_montadas

def execute_mkfs(args):
    particion_montada = None
    for particion in particiones_montadas:
        if particion[0] == args.id:
            particion_montada = particion
            break

    if particion_montada == None:
        print("Error: particion no montada")
    else:
        numerador = particion_montada[1].s - struct.calcsize(Superblock().getConst())
        denominador = 4 + struct.calcsize(Inode().getConst()) + 3 * struct.calcsize(Fileblock().getConst())
        temp = 0 if args.fs == "2fs" else 0
        n = math.floor(numerador / denominador)

        #creando superbloque
        new_superblock = Superblock()
        new_superblock.inodes_count = n
        new_superblock.blocks_count = 3 * n
        new_superblock.free_blocks_count = 3 * n
        new_superblock.free_inodes_count = n
        date = coding_str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), 16)
        new_superblock.mtime = date
        new_superblock.umtime = date
        new_superblock.mcount = 1
        new_superblock.inode_size = struct.calcsize(Inode().getConst())
        new_superblock.block_size = struct.calcsize(Fileblock().getConst())

        if args.fs == "2fs":
            create_ext2(n, particion_montada, new_superblock, date)
        elif args.fs == 3:
            pass


def create_ext2(n, mPartition, new_superblock, date):
    new_superblock.filesystem_type = 2
    new_superblock.bm_inode_start = mPartition[1].start + struct.calcsize(Superblock().getConst())
    new_superblock.bm_block_start = new_superblock.bm_inode_start + n
    new_superblock.inode_start = new_superblock.bm_block_start +    3 * n
    new_superblock.block_start = new_superblock.inode_start + n * struct.calcsize(Inode().getConst())

    new_superblock.free_inodes_count -= 1
    new_superblock.free_blocks_count -= 1
    new_superblock.free_inodes_count -= 1
    new_superblock.free_blocks_count -= 1

    Crr_file = open(mPartition[2], "rb+")
    #generarDatosDisco(Crr_file, mPartition[1].start, new_superblock)

    zero = b'\0'

    for i in range(n):
        generarDatosDiscoNormal(Crr_file, new_superblock.bm_inode_start + i, zero)    

    for i in range(3 * n):
        generarDatosDiscoNormal(Crr_file, new_superblock.bm_block_start + i, zero)

    new_inode = Inode()
    for i in range(n): 
        generarDatosDisco(Crr_file, new_superblock.inode_start + i * struct.calcsize(Inode().getConst()), new_inode)

    new_Fileblock = Fileblock()
    for i in range(3 * n):
        generarDatosDisco(Crr_file, new_superblock.block_start + i * struct.calcsize(Fileblock().getConst()), new_Fileblock)
    
    
    Inode0 = Inode()
    Inode0.i_uid = 1
    Inode0.i_gid = 1
    Inode0.i_size = 0
    Inode0.i_atime = date
    Inode0.i_ctime = date
    Inode0.i_mtime = date
    Inode0.i_type = b'\0'
    Inode0.i_perm = b'664'
    Inode0.i_block[0] = 0

    # . | 0
    # .. | 0
    # user.txt | 1
    #

    # contenido = Content()
    # contenido.get_infomation()

    Folderblock0 = Folderblock()
    Folderblock0.Content[0].b_inodo = 0
    Folderblock0.Content[0].b_name = b'.'
    Folderblock0.Content[1].b_inodo = 0
    Folderblock0.Content[1].b_name = b'..'
    Folderblock0.Content[2].b_inodo = 1
    Folderblock0.Content[2].b_name = b'user.txt'

    
    Inode1 = Inode()
    Inode1.i_uid = 1
    Inode1.i_gid = 1
    Inode1.i_size = struct.calcsize(Fileblock().getConst())
    Inode1.i_atime = date
    Inode1.i_ctime = date
    Inode1.i_mtime = date
    Inode1.i_type = b'1'
    Inode1.i_perm = b'664'
    Inode1.i_block[0] = 1


    data_usertxt = '1,G,root\n1,U,root,root,123\n'
    Fileblock1 = Fileblock()
    Fileblock1.b_content = coding_str(data_usertxt,64)

    generarDatosDisco(Crr_file, mPartition[1].start, new_superblock)
    
    # fill bitmap  inodes
    generarDatosDiscoNormal(Crr_file, new_superblock.bm_inode_start, b'\1')
    generarDatosDiscoNormal(Crr_file, new_superblock.bm_inode_start+1, b'\1')
    
    # fill bm blocks
    generarDatosDiscoNormal(Crr_file, new_superblock.bm_block_start, b'\1')
    generarDatosDiscoNormal(Crr_file, new_superblock.bm_block_start+1, b'\1')

    # fill inodes  
    generarDatosDisco(Crr_file, new_superblock.inode_start, Inode0)
    generarDatosDisco(Crr_file, new_superblock.inode_start+1*struct.calcsize(Inode().getConst()), Inode1)

    # fill blocks
    generarDatosDisco(Crr_file, new_superblock.block_start, Folderblock0)
    generarDatosDisco(Crr_file, new_superblock.block_start+1*struct.calcsize(Fileblock().getConst()), Fileblock1)

    Crr_file.close()
    print("Sistema de archivos creado exitosamente")
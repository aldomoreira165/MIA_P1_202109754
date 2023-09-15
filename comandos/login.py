from comandos.mount import particiones_montadas
from elementos.disco import *
from elementos.superbloque import Superblock
from elementos.inodo import Inode
from elementos.folderblock import Folderblock
from elementos.fileblock import Fileblock

userSesion = []

def execute_login(args):

    if len(userSesion) != 0:
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
            Crrfile = open(mPartition[2], "rb+")
            obtenerDatosDiscoAbierto(Crrfile, mPartition[1].start, TempSuperblock)
            IndexInode = initSearch("/user.txt",Crrfile,TempSuperblock)
            InodeFIle = Inode()
            obtenerDatosDiscoAbierto(Crrfile, TempSuperblock.inode_start + IndexInode * TempSuperblock.inode_size, InodeFIle)

            data = getInodeFileData(InodeFIle,Crrfile,TempSuperblock)
            splitData = data.split("\n")
            splitData.pop()

            for line in splitData:
                info = line.split(",")
                if info[1] == "U":
                    if info[2] == args.user:
                        print(userSesion)
                        userSesion.append(info)
                        pass
        
            print("=============")
            print("Sesion iniciada:", userSesion)
            Crrfile.close()

def initSearch(path,Crrfile,TempSuperblock):
    print("path",path)
    StepsPath = path.split("/")
    StepsPath.pop(0)
    
    if(len(StepsPath)==0):
        return 0
    
    print("StepsPath",StepsPath)
    Inode0 = Inode()
    obtenerDatosDiscoAbierto(Crrfile, TempSuperblock.inode_start, Inode0)
    return SarchInodeByPath(StepsPath,Inode0,Crrfile,TempSuperblock)

def SarchInodeByPath(StepsPath,Inode,Crrfile,TempSuperblock):
    index = 0 
    SearchedName = StepsPath.pop(0)
       
    for i in Inode.i_block:
        if(i != -1):
            if(index < 13):
                #CASO DIRECTOS
                crr_Folderblock = Folderblock()
                obtenerDatosDiscoAbierto(Crrfile, TempSuperblock.block_start + i * TempSuperblock.block_size, crr_Folderblock)

                for content in crr_Folderblock.Content:
                    if(content.b_inodo != -1):
                        if(content.b_name.decode() == SearchedName):
                            if(len(StepsPath)==0):
                                return content.b_inodo
                            else:
                                NextInode = Inode()
                                obtenerDatosDiscoAbierto(Crrfile, TempSuperblock.inode_start + content.b_inodo * TempSuperblock.inode_size, NextInode)
                                return SarchInodeByPath(StepsPath,NextInode,Crrfile)
    
            else:
                #CASO INDIRECTOS 
                pass  
        index+=1


    
def getInodeFileData(Inode,Crrfile,TempSuperblock):
    index = 0
    content = ""
    for i in Inode.i_block:
        if(i != -1):
            if(index < 13):
                #CASO DIRECTOS
                crr_Fileblock = Fileblock()
                obtenerDatosDiscoAbierto(Crrfile, TempSuperblock.block_start + i * TempSuperblock.block_size, crr_Fileblock)

                content += crr_Fileblock.b_content.decode()
    
            else:
                #CASO INDIRECTOS 
                pass  
        index+=1

    return content

def execute_logout():
    if len(userSesion) == 0:
        print("No existe una sesion iniciada")
    else:
        userSesion.clear()
        print("Sesion cerrada")
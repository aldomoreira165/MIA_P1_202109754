import os
from elementos.disco import *
from elementos.mbr import Mbr
from comandos.mount import particiones_montadas
from elementos.ebr import Ebr
from elementos.superbloque import Superblock

def execute_rep(args):
    if args.name == "mbr":
        reporte_mbr(args.path, args.id)
    elif args.name == "disk":
        reporte_disk(args.path, args.id)
    elif args.name == "sb":
        reporte_sb(args.path, args.id)

#sb
def reporte_sb(ruta, id):
    #abrir disco y obtener particion
    try:
        #buscar id en particiones montadas
        elemento_encontrado = None

        for elemento in particiones_montadas:
            if elemento[0] == id:
                elemento_encontrado = elemento
                break

        if elemento_encontrado == None:
            print("No se encontro la particion")
        else:
            mbrDisco = Mbr()
            obtenerDatosDisco(elemento_encontrado[2], 0, mbrDisco)
            superBloque = Superblock()
            obtenerDatosDisco(elemento_encontrado[2], mbrDisco.particion1.start, superBloque)
            dot = "digraph sb{\n"
            dot += "node [shape=plaintext]\n"
            dot += "table [label=<\n"
            dot += "<table border=\"1\" cellborder=\"1\" cellspacing=\"0\">\n"
            dot += "<tr><td colspan=\"3\" bgcolor=\"yellow\">Reporte de Superbloque</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_filesystem_type</td><td bgcolor=\"lightgray\">{superBloque.filesystem_type}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_inodes_count</td><td bgcolor=\"lightgray\">{superBloque.inodes_count}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_blocks_count</td><td bgcolor=\"lightgray\">{superBloque.blocks_count}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_free_blocks_count</td><td bgcolor=\"lightgray\">{superBloque.free_blocks_count}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_free_inodes_count</td><td bgcolor=\"lightgray\">{superBloque.free_inodes_count}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_mtime</td><td bgcolor=\"lightgray\">{superBloque.mtime}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_umtime</td><td bgcolor=\"lightgray\">{superBloque.umtime}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_mnt_count</td><td bgcolor=\"lightgray\">{superBloque.mcount}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_magic</td><td bgcolor=\"lightgray\">{superBloque.magic}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_inode_size</td><td bgcolor=\"lightgray\">{superBloque.inode_size}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_block_size</td><td bgcolor=\"lightgray\">{superBloque.block_size}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_first_ino</td><td bgcolor=\"lightgray\">{superBloque.first_ino}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_first_blo</td><td bgcolor=\"lightgray\">{superBloque.first_blo}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_bm_inode_start</td><td bgcolor=\"lightgray\">{superBloque.bm_inode_start}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_bm_block_start</td><td bgcolor=\"lightgray\">{superBloque.bm_block_start}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_inode_start</td><td bgcolor=\"lightgray\">{superBloque.inode_start}</td></tr>\n"
            dot += f"<tr><td bgcolor=\"lightgray\">s_block_start</td><td bgcolor=\"lightgray\">{superBloque.block_start}</td></tr>\n"
            dot += "</table>\n"
            dot += ">];\n"
            dot += "}"

            guardarImagen(ruta, dot)
    except Exception as e:
        print(f"Error: {e}")

#disk
def reporte_disk(ruta, id):
    #abrir disco y obtener particion
    try:
        #buscar id en particiones montadas
        elemento_encontrado = None

        for elemento in particiones_montadas:
            if elemento[0] == id:
                elemento_encontrado = elemento
                break

        if elemento_encontrado == None:
            print("No se encontro la particion")
        else:
            mbrDisco = Mbr()
            obtenerDatosDisco(elemento_encontrado[2], 0, mbrDisco)
            

            dot = "digraph D{\n"
            dot += "subgraph cluster_0 {\n"
            dot += "bgcolor=\"#68d9e2\"\n"
            dot += "node [style=\"rounded\" style=filled];\n"
            labelContent = labelDisk(elemento_encontrado[2], mbrDisco)
            dot += f"node_A [shape=record label=\"{labelContent}\"];\n"
            dot += "}\n"
            dot += "}"

            guardarImagen(ruta, dot)
    except Exception as e:
        print(f"Error: {e}")
            

#mbr
def reporte_mbr(ruta, id):
    #abrir disco y obtener particion
    try:
        #buscar id en particiones montadas
        elemento_encontrado = None

        for elemento in particiones_montadas:
            if elemento[0] == id:
                elemento_encontrado = elemento
                break

        if elemento_encontrado == None:
            print("No se encontro la particion")
        else:
            inicioEBR = -1
            mbrDisco = Mbr()
            obtenerDatosDisco(elemento_encontrado[2], 0, mbrDisco)

            #generando codigo .dot del mbr
            dot = "digraph mbr{\n"
            dot += "a0 [shape=none label=<\n"
            dot += "<TABLE cellspacing=\"10\" cellpadding=\"10\" style=\"rounded\" bgcolor=\"red\">\n"
            dot += dotMBR(mbrDisco)
            
            #generando codigo .dot de las particiones primarias
            dot += particionPrimaria(mbrDisco)

            #generando codigo .dot de los ebr en caso existan
            if mbrDisco.particion1.type == b'e':
                dot += dotExtendida(mbrDisco.particion1)
                inicioEBR = mbrDisco.particion1.start
            elif mbrDisco.particion2.type == b'e':
                dot += dotExtendida(mbrDisco.particion2)
                inicioEBR = mbrDisco.particion2.start
            elif mbrDisco.particion3.type == b'e':
                dot += dotExtendida(mbrDisco.particion3)
                inicioEBR = mbrDisco.particion3.start
            elif mbrDisco.particion4.type == b'e':
                dot += dotExtendida(mbrDisco.particion4)
                inicioEBR = mbrDisco.particion4.start

            if inicioEBR != -1:
                dot += dotLogica(elemento_encontrado[2], inicioEBR)
            
            dot += "</TABLE>>];\n"
            dot += "}"

            guardarImagen(ruta, dot)       
    except Exception as e:
        print(f"Error: {e}")

#funciones auxiliares disk
def labelDisk (rutaDisco, mbrDisco):
    etiqueta = ""

    etiqueta += f"MBR"
    
    if mbrDisco.particion1.type == b'p':
        porcentajePrimaria = round((mbrDisco.particion1.s / (mbrDisco.tamano)) * 100, 3) 
        etiqueta += f"| [P1] Primaria \\n {porcentajePrimaria} %"
    elif mbrDisco.particion1.type == b'e':
        etiqueta += "|{ [P1] Extendida "
        etiqueta += "|"
        etiqueta += "{"
        etiqueta += obtenerContenidoDisk(mbrDisco.particion1.start, rutaDisco, mbrDisco.tamano)
        etiqueta += "}"
        etiqueta += "}"
    else:
        etiqueta += "|[P1] Libre" 

    if mbrDisco.particion2.type == b'p':
        porcentajePrimaria = round((mbrDisco.particion2.s / (mbrDisco.tamano)) * 100, 3) 
        etiqueta += f"| [P2] Primaria \\n {porcentajePrimaria} %"
    elif mbrDisco.particion2.type == b'e':
        etiqueta += "|{ [P2] Extendida "
        etiqueta += "|"
        etiqueta += "{"
        etiqueta += obtenerContenidoDisk(mbrDisco.particion2.start, rutaDisco, mbrDisco.tamano)
        etiqueta += "}"
        etiqueta += "}"
    else:
        etiqueta += "|[P2] Libre"

    if mbrDisco.particion3.type == b'p':
        porcentajePrimaria = round((mbrDisco.particion3.s / (mbrDisco.tamano)) * 100, 3) 
        etiqueta += f"| [P3] Primaria \\n {porcentajePrimaria} %"
    elif mbrDisco.particion3.type == b'e':
        etiqueta += "|{ [P3] Extendida "
        etiqueta += "|"
        etiqueta += "{"
        etiqueta += obtenerContenidoDisk(mbrDisco.particion3.start, rutaDisco, mbrDisco.tamano)
        etiqueta += "}"
        etiqueta += "}"
    else:
        etiqueta += "|[P3] Libre"

    if mbrDisco.particion4.type == b'p':
        porcentajePrimaria = round((mbrDisco.particion4.s / (mbrDisco.tamano)) * 100, 3) 
        etiqueta += f" | [P4] Primaria \\n {porcentajePrimaria} %"
    elif mbrDisco.particion4.type == b'e':
        etiqueta += "|{ [P4] Extendida "
        etiqueta += "|"
        etiqueta += "{"
        etiqueta += obtenerContenidoDisk(mbrDisco.particion4.start, rutaDisco, mbrDisco.tamano)
        etiqueta += "}"
        etiqueta += "}"
    else:
        etiqueta += "|[P4] Libre"

    return etiqueta

def obtenerContenidoDisk(inicio, rutaDisco, sizeDisco):
    ebr = Ebr()
    obtenerDatosDisco(rutaDisco, inicio, ebr)
    etiqueta = graficarLogicas(ebr, sizeDisco, rutaDisco)
    return etiqueta
    
    
def graficarLogicas(ebr, size, rutaDisco):
    etiqueta = ""
    while ebr.next != -1:
        etiqueta += "EBR"
        porcentajeLogica = round((ebr.s / size) * 100, 3)
        etiqueta += f"| Logica \\n {porcentajeLogica} % |"
        obtenerDatosDisco(rutaDisco, ebr.next, ebr)
    etiqueta += "EBR"
    return etiqueta


#funciones auxiliares mbr
def dotMBR(mbrDisco):
    dot = ""
    dot += " <TR><TD bgcolor=\"yellow\">REPORTE MBR</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"yellow\">mbr_tamano</TD><TD bgcolor=\"yellow\">{mbrDisco.get_tamano()}</TD></TR>\n"
    dot += f" <TR><TD bgcolor=\"yellow\">mbr_fecha_creacion</TD><TD bgcolor=\"yellow\">{mbrDisco.get_time()}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"yellow\">mbr_disk_signature</TD><TD bgcolor=\"yellow\">{mbrDisco.get_dsk_signature()}</TD></TR>\n"
    return dot

def dotExtendida(particion):
    dot = ""
    dot += " <TR><TD bgcolor=\"blue\">PARTICION EXTENDIDA</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"blue\">part_status</TD><TD bgcolor=\"blue\">{particion.status}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"blue\">part_type</TD><TD bgcolor=\"blue\">{particion.type}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"blue\">part_fit</TD><TD bgcolor=\"blue\">{particion.fit}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"blue\">part_start</TD><TD bgcolor=\"blue\">{particion.start}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"blue\">part_size</TD><TD bgcolor=\"blue\">{particion.s}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"blue\">part_name</TD><TD bgcolor=\"blue\">{particion.name}</TD></TR>\n"
    return dot

def dotLogica(rutaDisco, puntero):
    with open(rutaDisco, "rb") as discoAbierto:
        discoAbierto.seek(puntero)
        ebr = Ebr()
        obtenerDatosDisco(rutaDisco, puntero, ebr)
        dot = ""
        dot += " <TR><TD bgcolor=\"green\">PARTICION LOGICA</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"green\">part_status</TD><TD bgcolor=\"green\">{ebr.status}</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"green\">part_fit</TD><TD bgcolor=\"green\">{ebr.fit}</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"green\">part_start</TD><TD bgcolor=\"green\">{ebr.start}</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"green\">part_size</TD><TD bgcolor=\"green\">{ebr.s}</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"green\">part_next</TD><TD bgcolor=\"green\">{ebr.next}</TD></TR>\n"
        dot += f"<TR><TD bgcolor=\"green\">part_name</TD><TD bgcolor=\"green\">{ebr.name}</TD></TR>\n"
        if ebr.next != -1:
            dot += dotLogica(rutaDisco, ebr.next)
        return dot
    
def particionPrimaria(mbr):
    dot = ""
    if mbr.particion1.type == b'p':
        dot += dotPrimaria(mbr.particion1)
    if mbr.particion2.type == b'p':
        dot += dotPrimaria(mbr.particion2)
    if mbr.particion3.type == b'p':
        dot += dotPrimaria(mbr.particion3)
    if mbr.particion4.type == b'p':
        dot += dotPrimaria(mbr.particion4)

    return dot
    
def dotPrimaria(particion):
    dot = ""
    dot += " <TR><TD bgcolor=\"pink\">PARTICION PRIMARIA</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"pink\">part_status</TD><TD bgcolor=\"pink\">{particion.status}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"pink\">part_type</TD><TD bgcolor=\"pink\">{particion.type}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"pink\">part_fit</TD><TD bgcolor=\"pink\">{particion.fit}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"pink\">part_start</TD><TD bgcolor=\"pink\">{particion.start}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"pink\">part_size</TD><TD bgcolor=\"pink\">{particion.s}</TD></TR>\n"
    dot += f"<TR><TD bgcolor=\"pink\">part_name</TD><TD bgcolor=\"pink\">{particion.name}</TD></TR>\n"
    return dot

def guardarImagen(ruta, dot):
    directorios = os.path.dirname(ruta)
    rutaCompleta, extension = os.path.splitext(ruta)
    #creando la ruta en caso no exista para almacenar la imagen
    if not os.path.exists(directorios):
        os.makedirs(directorios)
    
    #generar la imagen del mbr
    nombreDot = rutaCompleta + ".dot"
    f = open(nombreDot, "w")
    f.write(dot)
    f.close()

    nombreGraph = rutaCompleta + extension
    os.system(f"dot -Tpng {nombreDot} -o {nombreGraph}")
    os.system(f"{ruta}")